# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from polymorphic import PolymorphicModel
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

import datetime
import re
import json
import hashlib

from six.moves.urllib.error import URLError
from six.moves import urllib


class InvalidCharacterError(Exception):
    pass


class InvalidPBResponse(Exception):
    pass


def email_helper(user, tag, **context):
    context['username'] = user.username
    subject = render_to_string('pbspy/email_{tag}_subject.txt'.format(tag=tag), context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message  = render_to_string('pbspy/email_{tag}.txt'.format(tag=tag), context)
    user.email_user(subject, message)


# NOTE: Year is stored as number (should be integer but actually float) with month prefix
# 1000 BC => -1000
# 500 AD => 500
# January, 2050 AD => 12050
# July, 2044 AD => 72044
def format_year(number):
    if number is None:
        return None
    if number >= 0:
        if number >= 10000:
            year = int(number % 10000)
            imonth = int(number / 10000)
            if imonth == 1:
                month = _('January')
            elif imonth == 7:
                month = _('July')
            else:
                raise ValueError('Invalid month for format_year')
            return _("{month}, {year} AD").format(month=month, year=year)

        return _("{year} AD").format(year=int(number))
    return _("{year} BC").format(year=-int(number))


def parse_year(year_str):
    try:
        (year, qual) = year_str.split()
        year = int(year)
    except ValueError:
        (month, year, qual) = year_str.split()
        if month.lower().find('jan'):
            imonth = 1
        elif month.lower().find('jul'):
            imonth = 7
        else:
            raise ValueError('Failed to parse month part of date')
        year = int(year) + 10000 * imonth

    if qual == 'AD':
        return year
    elif qual == 'BC':
        return -year
    else:
        raise ValueError('invalid year suffix')

savegame_allowed_name_re = re.compile('^[0-9a-zA-Z_\-][0-9a-zA-Z_\.\-]*\Z')


class Game(models.Model):
    pb_remote_password = models.CharField(max_length=200)
    create_date        = models.DateTimeField(auto_now_add=True)
    name               = models.CharField(max_length=200, unique=True)
    hostname           = models.CharField(max_length=200)
    port               = models.PositiveIntegerField(
        default=2056,
        validators=[MaxValueValidator(65535), MinValueValidator(1)]
    )
    manage_port        = models.PositiveIntegerField(
        default=13373,
        validators=[MaxValueValidator(65535), MinValueValidator(1)]
    )
    description        = models.TextField(blank=True, null=True)
    url                = models.CharField(max_length=200, blank=True, null=True,
                                          validators=[URLValidator()])

    # Timestamp of last successful connection. Field is null if the game was never connected.
    last_update_successful = models.DateTimeField(null=True)
    # Timestamp of last connection attempt. Will be used to  omit multiple connection attempts.
    # FIXME: Add default, DO NOT use now() as this will repetedly create migrations
    last_update_attempt = models.DateTimeField(null=False)

    is_paused          = models.BooleanField(default=False)
    is_headless        = models.BooleanField(default=False)
    is_autostart       = models.BooleanField(default=True)
    year               = models.IntegerField(blank=True, null=True)
    pb_name            = models.CharField(blank=True, null=True, max_length=200)
    turn               = models.PositiveSmallIntegerField(default=0)
    # In hours
    timer_max_h        = models.PositiveIntegerField(blank=True, null=True)
    # In seconds!
    timer_remaining_4s = models.PositiveIntegerField(blank=True, null=True)

    admins             = models.ManyToManyField(User, related_name='admin_games')
    is_private         = models.BooleanField(default=False)
    is_online          = models.BooleanField(default=True)
    #This values has to set manually by Admins
    is_finished        = models.BooleanField(default=False)
    victory_player_id  = models.SmallIntegerField(default=-1)
    victory_type       = models.SmallIntegerField(default=-1)

    subscribed_users   = models.ManyToManyField(User, related_name='subscribed_games')

    def auth_hash(self):
        return hashlib.md5(self.pb_remote_password.encode()).hexdigest()

    def timer(self):
        return self.timer_max_h is not None

    def timer_end(self):
        delta = datetime.timedelta(seconds=round(self.timer_remaining_4s / 4))
        return self.last_update_successful + delta

    # Estimate end in realtime (PB clock runs slower).
    # TODO find better way to estimate e.g. interpolate from log
    def timer_end_realtime(self):
        delta = datetime.timedelta(seconds=round(self.timer_remaining_4s / 4))
        return self.last_update_successful + delta * 5 / 4

    def year_str(self):
        return format_year(self.year)

    def can_manage(self, user):
        return len(self.admins.filter(id=user.id)) == 1

    def can_view(self, user):
        return (not self.is_private) or (len(self.admins.filter(id=user.id)) == 1)

    def get_status(self):
        if self.is_finished:
            return "finished"
        else:
            if self.is_online:
                return "online"
            else:
                return "offline"

    def get_last_activity(self):
        return self.last_update_attempt

    def get_online_players(self):
        if not self.is_online:
            return []
        return self.player_set.all().filter(is_online=True)

    def refresh(self, min_time_diff=60, ignore_game_state=False):
        """
        Check timestamp and request new data from pb server
        if we assume newer data.
        """
        if not ignore_game_state and not self.is_online:
            return
        if not ignore_game_state and self.is_finished:
            return
        cur_date = timezone.now()
        delta = datetime.timedelta(seconds=min_time_diff)
        if cur_date < self.last_update_attempt + delta:
            return
        try:
            info = self.pb_info()
            self.set_from_dict(info)
        except (InvalidPBResponse, URLError):
            if self.is_online:
                self.is_online = False
                self.save()
            elif ignore_game_state:
                self.last_update_attempt = cur_date
                self.save()
            return


    @transaction.atomic
    def set_from_dict(self, info):
        date = timezone.now()

        # Minimal alive messages do not contain
        # all fields.
        # FIXME bMinimal - bad logic structure
        bMinimal = (info.get('gameName') == None)

        is_online = True
        if info['turnTimer']:
            if 'turnTimerMax' in info:
                timer_max_h = int(info['turnTimerMax'])
            else:
                timer_max_h = self.timer_max_h
            timer_remaining_4s = int(info['turnTimerValue'])
        else:
            timer_max_h        = None
            timer_remaining_4s = None

        if not bMinimal:
            year      = parse_year(info['gameDate'])
            turn      = int(info['gameTurn'])
            is_paused = bool(info['bPaused'])
            is_headless = bool(info['bHeadless'])
            is_autostart = bool(info['bAutostart'])
            pb_name   = info['gameName']

            logargs = {'game': self, 'date': date,
                       'year': year, 'turn': turn}


            player_count_old = self.player_set.count()
            player_count = len(info['players'])
            if (self.pb_name != info['gameName'] or
                    player_count_old != player_count):
                GameLogMetaChange(
                    pb_name_old=self.pb_name,
                    pb_name=info['gameName'],
                    player_count_old=player_count_old,
                    player_count=player_count,
                    **logargs).save()
                #Remove player list of old game
                if player_count_old > 0:
                    self.player_set.all().delete()

            if turn > self.turn:
                mt = GameLogMissedTurn(**logargs)
                mt.set_missed_players(self.player_set.all())
                if mt.is_turn_incomplete():
                    mt.save()
                GameLogTurn(**logargs).save()
                self.send_new_turn_info()
            elif (turn < self.turn or
                    (timer_remaining_4s is not None and
                     self.timer_remaining_4s is not None and
                     timer_remaining_4s > self.timer_remaining_4s + 1200 / 4)):
                # TODO find a better way than to hardcode the value
                #Note: Ignore small time difference because every combat increase
                # the timer by the combat animation time
                GameLogReload(**logargs).save()

            if is_paused != self.is_paused:
                GameLogPause(paused=is_paused, **logargs).save()

            if is_headless != self.is_headless:
                pass

            if is_autostart != self.is_autostart:
                pass

            if is_online != self.is_online:
                pass

            if timer_max_h != self.timer_max_h:
                GameLogTimerChanged(timer_max_h=timer_max_h, **logargs).save()

            # FIXME Where does this belong?
            self.timer_max_h        = timer_max_h
            self.timer_remaining_4s = timer_remaining_4s

        if not bMinimal:
            self.last_update_successful = date
            self.last_update_attempt = date
            self.pb_name            = pb_name
            self.turn               = turn
            self.is_paused          = is_paused
            self.is_headless        = is_headless
            self.is_autostart       = is_autostart
            self.year               = year
            self.is_online          = is_online

        self.save()

        if not bMinimal:
            for player_info in info['players']:
                try:
                    player = self.player_set.get(ingame_id=player_info['id'])
                except Player.DoesNotExist:
                    player = Player(ingame_id=player_info['id'], game=self)
                player.set_from_dict(player_info, logargs)

    def pb_action(self, **kwargs):
        url = "http://{}:{}/api/v1/".format(self.hostname, self.manage_port)
        values = kwargs
        if not 'password' in values:
            values['password'] = self.pb_remote_password
        json_data = json.dumps(values)
        # should we maybe use 'ascii' or the default 'utf-8'
        data = urllib.parse.urlencode({json_data: None}).encode()

        headers = {'Content-Type': 'application/json'}
        # Note: urllib will add Content-Length and a nice user-agent for us

        # TODO proper exception handling
        request = urllib.request.Request(url, data, headers)
        try:
            response = urllib.request.urlopen(request, timeout=20)
        except URLError:
            raise InvalidPBResponse(_("Failed to connect to server."))

        # which decoding? Let's just hope default (probably utf-8) is ok
        ret_str = response.read().decode()
        ret = json.loads(ret_str)
        if ret['return'] != 'ok':
            # some info may be in ret['info'], but I don't want to leak anything
            raise InvalidPBResponse(ret)
        return ret

    def pb_info(self):
        result = self.pb_action(action='info')
        return result['info']

    def pb_chat(self, message, user=None):
        try:
            name = user.username
        except AttributeError:
            name = 'unknown'
        text = "{}: {}".format(name, message)
        return self.pb_action(action='chat', msg=text)

    def pb_set_motd(self, message, user=None):
        return self.pb_action(action='setMotD', msg=str(message))

    def pb_short_names(self, short_name_len, short_name_sdec, user=None):
        return self.pb_action(action='setShortNames', enable=(short_name_len > 0),
                              maxLenName=int(short_name_len), maxLenDesc=int(short_name_sdec))

    def pb_set_autostart(self, value, user=None):
        return self.pb_action(action='setAutostart', value=bool(value))

    def pb_set_headless(self, value, user=None):
        return self.pb_action(action='setHeadless', value=bool(value))

    def pb_save(self, filename, user=None):
        if not savegame_allowed_name_re.match(filename):
            raise InvalidCharacterError()
        result = self.pb_action(action='save', filename=filename)
        GameLogAdminSave(game=self, user=user, date=timezone.now(),
                         year=self.year, turn=self.turn,
                         filename=filename).save()
        return result

    def pb_set_current_turn_timer(self, hours, minutes, seconds, user=None):
        return self.pb_action(action='setCurrentTurnTimer', hours=int(hours),
                              minutes=int(minutes), seconds=int(seconds))

    def pb_set_turn_timer(self, value, user=None):
        return self.pb_action(action='setTurnTimer', value=int(value))

    def pb_set_pause(self, value, user=None):
        value = bool(value)
        result = self.pb_action(action='setPause', value=value)
        GameLogAdminPause(game=self, user=user, date=timezone.now(), paused=value,
                          year=self.year, turn=self.turn).save()
        if result['return'] == 'ok':
            self.is_paused = True
            self.save()
        return result

    def pb_end_turn(self, user=None):
        return self.pb_action(action='endTurn')

    def pb_restart(self, filename, folder_index=0, user=None):
        return self.pb_action(action='restart', filename=filename, folder_index=folder_index)

    def pb_set_player_password(self, player_obj, new_password, user=None):
        if not isinstance(player_obj, Player):
            raise InvalidPBResponse(_("No valid player given."))
        ingame_id = player_obj.ingame_id
        return self.pb_action(action='setPlayerPassword',
                              playerId=ingame_id, newCivPW=new_password)

    def pb_set_player_color(self, ingame_player_id, new_color, user=None):
        return self.pb_action(action='setPlayerColor', playerId=ingame_player_id, colorId=new_color)

    def pb_list_saves(self, user=None):
        result = self.pb_action(action='listSaves')
        return result['list']

    def pb_get_motd(self):
        #Wrap in try to respect older mod versions
        try:
            result = self.pb_action(action='getMotD')
            return str(result.get('msg', ''))
        except InvalidPBResponse:
            return ''

    def pb_list_colors(self):
        #Wrap in try to respect older mod versions
        try:
            result = self.pb_action(action='listPlayerColors')
            # Add id for template usage
            id = 0
            for c in result['colors']:
                c['id'] = id
                id += 1
            return result['colors']
        except InvalidPBResponse:
            return []

    def force_diconnect(self):
        GameLogForceDisconnect(game=self, date=timezone.now(), year=self.year, turn=self.turn).save()

    def update(self):
        info = self.pb_info()
        self.set_from_dict(info)

    def clean(self):
        # Disable validation to allow changes of offline
        # games.
        # The validation is still required for game creation
        # (see game_create(request) in views.py)
        # to prevent UDP flood attacks on other servers.
        #self.validate_connection()
        pass

    def validate_connection(self):
        # This will raise InvalidPBResponse or something else when we cannot connect
        try:
            info = self.pb_info()
        except InvalidPBResponse:
            raise ValidationError("Invalid response from the pitboss management interface. Possibly invalid password.")
        except URLError:
            raise ValidationError("Could not connect to the pitboss management interface.")

    def subscribe_user(self, user):
        self.subscribed_users.add(user)
        email_helper(user, 'subscribed',
                     game_name=self.name, game_pb_name=self.pb_name,
                     manage_url=reverse('game_detail', args=[self.id]))
        return _("You will now receive turn emails for this game on at {email}.").format(email=user.email)

    def unsubscribe_user(self, user):
        self.subscribed_users.remove(user)
        return _("You will no longer receive new turn emails for this game at {email}").format(email=user.email)

    def send_new_turn_info(self):
        for user in self.subscribed_users.all():
            email_helper(user, 'new_turn',
                         game_name=self.name, game_pb_name=self.pb_name, turn=self.turn,
                         manage_url=reverse('game_detail', args=[self.id]))

    def __str__(self):
        return self.name


class Color():
    def __init__(self, rgbstr):
        darkness = 0
        try:
            rgb = rgbstr.split(',')
            self.web = "#"
            for idx in range(0, 3):
                comp = int(rgb[idx])
                darkness += comp
                self.web = self.web + "{0:02x}".format(max(0, min(comp)))
        except ValueError:
            self.web = "#FF00FE"
        except IndexError:
            self.web = "#FF00FF"

        self.is_dark = darkness > 380


class Player(models.Model):
    # We leave it Django to make us a nice auto/unique PK for ForeignKey
    # Allthough it would be nice to have a composite primary key (game, ingame_id).
    # https://github.com/simone/django-compositekey doesn't work with Django 1.7 / Python3
    # Id as a fieldname is not allowed except for primary keys
    ingame_id     = models.PositiveSmallIntegerField()
    game          = models.ForeignKey(Game, db_index=True)

    name          = models.TextField(max_length=200)
    score         = models.PositiveIntegerField()
    finished_turn = models.BooleanField(default=False)
    # This is more like the status (e.g. AI, Offline)
    ping          = models.TextField(max_length=200, verbose_name='connection status')
    is_human      = models.BooleanField(default=False)
    is_claimed    = models.BooleanField(default=False)
    is_online     = models.BooleanField(default=False)
    civilization  = models.TextField(max_length=200)
    leader        = models.TextField(max_length=200)
    # Formatted as "RRR,GGG,BBB" decimal
    color_rgb     = models.TextField(max_length=3 * 3 + 2)

    def status(self):
        if self.score == 0:
            return _('eliminated')
        if not self.is_claimed:
            return _('unclaimed')
        if not self.is_human:
            return _('AI')
        if self.is_online:
            return _('online')
        return _('offline')

    def set_from_dict(self, info, logargs):
        logargs['player'] = self
        logargs['player_name'] = self.name

        score    = int(info['score'])
        # for online players ping is " [123 ms]"
        is_online = info['ping'][1] == '['

        # don't crate log entries for first entry
        if self.id is not None:
            if info['bClaimed'] and not self.is_claimed:
                GameLogClaimed(**logargs).save()

            if self.name != info['name']:
                GameLogNameChange(player_name_new=info['name'], **logargs).save()
                logargs['player_name'] = info['name']

            if not info['bHuman'] and self.is_human and score != 0:
                GameLogAI(**logargs).save()

            if is_online and not self.is_online:
                GameLogLogin(**logargs).save()

            if self.score != score:
                if score > 0:
                    GameLogScore(score=score, delta=(score - self.score), **logargs).save()
                else:
                    GameLogEliminated(**logargs).save()

            if (not self.finished_turn) and info['finishedTurn'] and self.is_human:
                GameLogFinish(**logargs).save()

            if not is_online and self.is_online:
                GameLogLogout(**logargs).save()

        self.name          = info['name']
        self.score         = score
        self.finished_turn = info['finishedTurn']
    #    if self.ping == "" info['ping'] == "Disconnected":
        self.ping          = info['ping']
        self.is_human      = info['bHuman']
        self.is_online     = is_online
        self.is_claimed    = info['bClaimed']
        self.civilization  = info['civilization']
        self.leader        = info['leader']
        self.color_rgb     = info['color']
        self.save()

    @property
    def color(self):
        return Color(self.color_rgb)

    class Meta:
        unique_together = (('ingame_id', 'game'),)
        index_together  = (('ingame_id', 'game'),)

    def __str__(self):
        return _("{} ({} of {})").format(self.name, self.leader, self.civilization)

    # Required for python2.x and umlautes
    def __unicode__(self):
        return _("{} ({} of {})").format(self.name, self.leader, self.civilization)


class GameLog(PolymorphicModel):
    game = models.ForeignKey(Game)
    date = models.DateTimeField(db_index=True)
    year = models.IntegerField()
    turn = models.PositiveSmallIntegerField()
    text = "(GameLog) No text defined."
    is_public = True # non-public log entries are for admins, only.

    def message(self):
        return _(self.text)

    def __str__(self):
        return _("{date}/{year}/turn {turn}: ").\
            format(date=self.date, year=format_year(self.year),
                   turn=self.turn) + self.message()

    @classmethod
    def generate_generic_log_type_name(cls):
        cname = cls.__name__
        logtype = cname.replace('GameLog', '', 1)

        def get_log_name():
            return logtype

        return get_log_name

    def get_log_name(self):
        self.get_log_name = self.generate_generic_log_type_name()
        return self.get_log_name()


class GameLogTurn(GameLog):
    def message(self):
        return _("A new turn has begun. It is now {year}").\
            format(year=format_year(self.year))

    # Example how to set the displayed name manually.
    """
    @classmethod
    def generateGenericLogTypeName(arg):
      def getLogName():
        return "The name of this type of log message.";
      return getLogName
    """


class GameLogReload(GameLog):
    def message(self):
        return _("The game was reloaded on year {year}").\
            format(year=format_year(self.year))


class GameLogMetaChange(GameLog):
    pb_name_old      = models.CharField(max_length=200, null=True)
    pb_name          = models.CharField(max_length=200)
    player_count_old = models.SmallIntegerField()
    player_count     = models.SmallIntegerField()

    def message(self):
        return _("A game named {name} was started with {num_players} players.").\
            format(name=self.pb_name, num_players=self.player_count)


class GameLogTimerChanged(GameLog):
    timer_max_h = models.PositiveSmallIntegerField(blank=True, null=True)

    def message(self):
        if self.timer_max_h is not None:
            return _("Turn timer changed to {timer} hours.").\
                format(timer=self.timer_max_h)
        return _("Turn timer disabled.")


class GameLogPause(GameLog):
    paused = models.BooleanField(default=None)

    def message(self):
        if self.paused:
            return _("Game paused by player.")
        else:
            return _("Game resumed by player.")


class GameLogServerTimeout(GameLog):
    def message(self):
        return _("Server timed out.")


class GameLogPlayer(GameLog):
    player_name = models.CharField(max_length=200)
    player      = models.ForeignKey(Player)

    def __str__(self):
        return _("{date}/{year}/turn {turn}, {player}: ").\
            format(date=self.date, year=format_year(self.year),
                   turn=self.turn,
                   player=self.player_name) + self.message()


class GameLogLogin(GameLogPlayer):
    text = "Logged in"


class GameLogLogout(GameLogPlayer):
    text = "Logged out"


class GameLogFinish(GameLogPlayer):
    text = "Finished turn"


class GameLogScore(GameLogPlayer):
    score = models.PositiveIntegerField()
    delta = models.IntegerField(default=0)

    def message(self):
        if self.delta > 0:
            return _("Score increased to {score} ({delta:+})").format(score=self.score, delta=self.delta)
        elif self.delta < 0:
            return _("Score decreased to {score} ({delta})").format(score=self.score, delta=self.delta)
        else:
            return _("Score changed to {score}").format(score=self.score)


class GameLogNameChange(GameLogPlayer):
    player_name_new = models.CharField(max_length=200)

    def message(self):
        return _("Changed name to {new_name}").format(new_name=self.player_name_new)


class GameLogEliminated(GameLogPlayer):
    text = "Eliminated"


class GameLogAI(GameLogPlayer):
    text = "Converted to AI"


class GameLogClaimed(GameLogPlayer):
    text = "Claimed"


class GameLogAdminAction(GameLog):
    user = models.ForeignKey(User, blank=True, null=True)

    def get_username(self):
        try:
            return self.user.username
        except AttributeError:
            return _("unknown user")


class GameLogAdminSave(GameLogAdminAction):
    filename = models.CharField(max_length=200)
    bPublic = False

    def message(self):
        return _("Game saved by {username}").format(username=self.get_username())


class GameLogAdminPause(GameLogAdminAction):
    paused = models.BooleanField(default=None)

    def message(self):
        if self.paused:
            return _("Pause activated by {username}").\
                format(username=self.get_username())
        else:
            return _("Pause deactivated by {username}").\
                format(username=self.get_username())


class GameLogAdminEndTurn(GameLogAdminAction):
    def message(self):
        return _("Turn ended by {username}").format(username=self.get_username())


class GameLogForceDisconnect(GameLog):
    def message(self):
        return _("A player was disconnected due to the upload-bug.")


class GameLogMissedTurn(GameLog):
    missed_turn_names = models.CharField(max_length=2000)
    missed_turn_ids = models.CommaSeparatedIntegerField(max_length=200)
    is_public = True

    # The integration of set_missed_players into the constructor
    # creates conflicts with the polymorphic stuff. Thus, I separeted both (Ramk)
    #def __init__(self, *args, **kwargs):
    #    super(GameLogMissedTurn, self).__init__(bPublic=False,*args, **kwargs)

    def set_missed_players(self, players):
        missed = []
        for player in players:
            # Player is online if ping string contains '['
            if not player.finished_turn and not player.ping[1] == '[':
                missed.append((str(player.ingame_id), str(player.name)))
        if len(missed) > 0:
            self.missed_turn_names = ",".join(list(zip(*missed))[1])
            self.missed_turn_ids = ",".join(list(zip(*missed))[0])
        else:
            self.missed_turn_names = ""
            self.missed_turn_ids = ""

    def is_turn_incomplete(self):
        return len(self.missed_turn_names)>0

    def message(self):
        format_names = []
        names = self.missed_turn_names.split(",")
        ids = self.missed_turn_ids.split(",")
        for (player_name, player_id) in zip(names, ids):
            format_names.append(_("<li>{} (Id={})</li>").format(player_name, player_id))
        return _("The following players did not finished their turn:") + "<ul>{players}</ul>".\
            format(players="\r\n".join(format_names))
