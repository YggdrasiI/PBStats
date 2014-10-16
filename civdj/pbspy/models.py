from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from polymorphic import PolymorphicModel
from django.utils import timezone
from django.contrib.auth.models import User

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

    update_date        = models.DateTimeField(blank=True, null=True)
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

    admins             = models.ManyToManyField(User)
    is_private         = models.BooleanField(default=False)

    def auth_hash(self):
        return hashlib.md5(self.pb_remote_password.encode()).hexdigest()

    def timer(self):
        return self.timer_max_h is not None

    def timer_end(self):
        delta = datetime.timedelta(seconds=round(self.timer_remaining_4s / 4))
        print(self.update_date + delta)
        return self.update_date + delta

    def year_str(self):
        return format_year(self.year)

    def can_manage(self, user):
        return len(self.admins.filter(id=user.id)) == 1

    def can_view(self, user):
        return (not self.is_private) or (len(self.admins.filter(id=user.id)) == 1)

    @transaction.atomic
    def set_from_dict(self, info):
        date = timezone.now()

        year      = parse_year(info['gameDate'])
        turn      = int(info['gameTurn'])
        is_paused = bool(info['bPaused'])
        is_headless = bool(info['bHeadless'])
        is_autostart = bool(info['bAutostart'])
        pb_name   = info['gameName']

        logargs = {'game': self, 'date': date,
                   'year': year, 'turn': turn}

        if info['turnTimer']:
            timer_max_h        = int(info['turnTimerMax'])
            timer_remaining_4s = int(info['turnTimerValue'])
        else:
            timer_max_h        = None
            timer_remaining_4s = None

        if timer_max_h != self.timer_max_h:
            GameLogTimerChanged(timer_max_h=timer_max_h, **logargs).save()

        player_count_old = self.player_set.count()
        if (self.pb_name != info['gameName'] or
                player_count_old != len(info['players'])):
            GameLogMetaChange(pb_name_old=self.pb_name, pb_name=info['gameName'],
                              player_count_old=player_count_old,
                              player_count=len(info['players'])).save()

        if turn > self.turn:
            GameLogTurn(**logargs).save()
        elif (turn < self.turn or
                (timer_remaining_4s is not None and
                 self.timer_remaining_4s is not None and
                 timer_remaining_4s > self.timer_remaining_4s)):
            GameLogReload(**logargs).save()

        if is_paused != self.is_paused:
            GameLogPause(paused=is_paused, **logargs).save()

        if is_headless != self.is_headless:
          pass

        if is_autostart != self.is_autostart:
          pass

        self.timer_max_h        = timer_max_h
        self.timer_remaining_4s = timer_remaining_4s
        self.update_date        = date
        self.pb_name            = pb_name
        self.turn               = turn
        self.is_paused          = is_paused
        self.is_headless        = is_headless
        self.is_autostart       = is_autostart
        self.year               = year
        self.save()

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
        data = urllib.parse.urlencode({json_data : None}).encode()

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

    def pb_motd(self, message, user=None):
        return self.pb_action(action='setMotD', msg=str(message))

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

    def pb_set_turn_timer(self, value, user=None):
        return self.pb_action(action='setTurnTimer', value=int(value))

    def pb_set_pause(self, value, user=None):
        value = bool(value)
        result = self.pb_action(action='setPause', value=value)
        GameLogAdminPause(game=self, user=user, date=timezone.now(), paused=value,
                          year=self.year, turn=self.turn).save()
        return result

    def pb_end_turn(self, user=None):
        return self.pb_action(action='endTurn')

    def pb_restart(self, filename, folderIndex=0, user=None):
        return self.pb_action(action='restart', filename=filename, folderIndex=folderIndex)

    def pb_set_player_password(self, player_id, new_password, user=None):
        if isinstance(player_id, Player):
            player_id = player_id.ingame_id
        return self.pb_action(action='setPlayerPassword',
                              playerId=player_id, newCivPW=new_password)

    def pb_list_saves(self, user=None):
        result = self.pb_action(action='listSaves')
        return result['list']

    def force_diconnect(self):
        GameLogForceDisconnect(game=self, date=timezone.now(), year=self.year, turn=self.turn).save()

    def update(self):
        info = self.pb_info()
        self.set_from_dict(info)

    def clean(self):
        self.validate_connection()

    def validate_connection(self):
        # This will raise InvalidPBResponse or something else when we cannot connect
        try:
            info = self.pb_info()
        except InvalidPBResponse as e:
            raise ValidationError("Invalid response from the pitboss management interface. Possibly invalid password.")
        except URLError as e:
            raise ValidationError("Could not connect to the pitboss management interface.")

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
        if not self.is_claimed:
            return _('unclaimed')
        if self.score == 0:
            return _('eliminated')
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
                    GameLogScore(score=score, increase=(score > self.score), **logargs).save()
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

class GameLog(PolymorphicModel):
    game = models.ForeignKey(Game)
    date = models.DateTimeField(db_index=True)
    year = models.IntegerField()
    turn = models.PositiveSmallIntegerField()

    def message(self):
        return _(self.text)

    def __str__(self):
        return _("{date}/{year}/turn {turn}: {message}").\
            format(date=self.date, year=format_year(self.year),
                   turn=self.turn, message=self.message())

    """
    def generateGenericLogTypeName(self):
      cname = self.__class__.__name__
      logtype = cname.replace('GameLog','',1)
      def getLogName():
        return logtype
      return getLogName

    def getLogName(self):
      self.getLogName = self.generateGenericLogTypeName()
      return self.getLogName()
    """

    #@staticmethod
    @classmethod
    def generateGenericLogTypeName(arg):
      #cname = __class__.__name__
      cname = arg.__name__
      logtype = cname.replace('GameLog','',1)
      def getLogName():
        return logtype
      return getLogName

    def getLogName(self):
      self.getLogName = self.generateGenericLogTypeName()
      return self.getLogName()


class GameLogTurn(GameLog):
    def message(self):
        return _("A new turn has begun. It is now {year}").\
            format(year=format_year(self.year))


class GameLogReload(GameLog):
    def message(self):
        return _("The game was reloaded on year {year}").\
            format(year=format_year(self.year))


class GameLogMetaChange(GameLog):
    pb_name_old      = models.CharField(max_length=200)
    pb_name          = models.CharField(max_length=200)
    player_count_old = models.SmallIntegerField()
    player_count     = models.SmallIntegerField()

    def message(self):
        return _("A game named {name} was started with {num_players} players.").\
            format(name=self.game_name_new, num_players=self.num_players_new)


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
        return _("{date}/{year}/turn {turn}, {player}: {message}").\
            format(date=self.date, year=format_year(self.year),
                   turn=self.turn, player=self.player_name, message=self.message())


class GameLogLogin(GameLogPlayer):
    text = "Logged in"


class GameLogLogout(GameLogPlayer):
    text = "Logged out"


class GameLogFinish(GameLogPlayer):
    text = "Finished turn"


class GameLogScore(GameLogPlayer):
    score = models.PositiveIntegerField()
    increase = models.BooleanField(default=None)

    def message(self):
        if self.increase:
            return _("Score increased to {score}").format(score=self.score)
        else:
            return _("Score decreased to {score}").format(score=self.score)


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

