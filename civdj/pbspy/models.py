from django.utils.translation import ugettext as _
from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator
from polymorphic import PolymorphicModel
from django.utils import timezone

import datetime

def format_year(number):
    if number is None:
        return None
    if number >= 0:
        return _("{year} AD").format(year=number)
    return _("{year} BC").format(year=-number)


def parse_year(year_str):
    (year, qual) = year_str.split(' ')
    year = int(year)
    if qual == 'AD':
        return year
    elif qual == 'BC':
        return -year
    else:
        raise ValueError('invalid year suffix')


class Game(models.Model):
    auth_token_hash = models.CharField(max_length=200)
    create_date     = models.DateTimeField(auto_now_add=True)
    name            = models.CharField(max_length=200, unique=True)
    hostname        = models.CharField(max_length=200)
    port            = models.PositiveIntegerField(
        default=2056,
        validators=[MaxValueValidator(65535), MinValueValidator(1)]
    )
    manage_port     = models.PositiveIntegerField(
        default=13373,
        validators=[MaxValueValidator(65535), MinValueValidator(1)]
    )
    description     = models.TextField(blank=True, null=True)
    url             = models.CharField(max_length=200, blank=True, null=True)

    update_date     = models.DateTimeField(blank=True, null=True)
    is_paused       = models.BooleanField(default=False)
    year            = models.FloatField(blank=True, null=True)
    pb_name         = models.CharField(blank=True, null=True, max_length=200)
    turn            = models.PositiveSmallIntegerField(default=0)
    # In hours
    timer_max_h     = models.PositiveIntegerField(blank=True, null=True)
    # In seconds!
    timer_remaining_4s = models.PositiveIntegerField(blank=True, null=True)

    def timer(self):
        return self.timer_max_h is not None

    def timer_end(self):
        delta = datetime.timedelta(seconds=round(self.timer_remaining_4s / 4))
        print(self.update_date + delta)
        return self.update_date + delta

    def year_str(self):
        return format_year(self.year)

    @transaction.atomic
    def set_from_dict(self, info):
        date = timezone.now()

        year      = parse_year(info['gameDate'])
        turn      = int(info['gameTurn'])
        is_paused = bool(info['bPaused'])
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
                              player_count=len(info['players']))

        if turn > self.turn:
            GameLogTurn(**logargs).save()
        elif (turn < self.turn or
                (timer_remaining_4s is not None and self.timer_remaining_4s is not None and
                 timer_remaining_4s > self.timer_remaining_4s)):
            GameLogReload(**logargs).save()

        if is_paused != self.is_paused:
            GameLogPause(paused=is_paused, **logargs).save()

        self.timer_max_h        = timer_max_h
        self.timer_remaining_4s = timer_remaining_4s
        self.update_date        = date
        self.pb_name            = pb_name
        self.turn               = turn
        self.is_paused          = is_paused
        self.year               = year
        self.save()

        for player_info in info['players']:
            try:
                player = self.player_set.get(ingame_id=player_info['id'])
            except Player.DoesNotExist:
                player = Player(ingame_id=player_info['id'], game=self)
            player.set_from_dict(player_info, logargs)

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
#        if not self.is_claimed:
#            return _('unclaimed')
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

            if not info['bHuman'] and self.is_human:
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


class GameLog(PolymorphicModel):
    game = models.ForeignKey(Game)
    date = models.DateTimeField(db_index=True)
    year = models.SmallIntegerField()
    turn = models.PositiveSmallIntegerField()

    def message(self):
        return _(self.text)

    def __str__(self):
        return _("{date}/{year}/turn {turn}: {message}").\
            format(date=self.date, year=format_year(self.year),
                   turn=self.turn, message=self.message())


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
            return _("Game paused.")
        else:
            return _("Game resumed")


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
