from django.utils.translation import ugettext as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from polymorphic import PolymorphicModel


def format_year(number):
    if number >= 0:
        return _("{year} AD").format(year=number)
    return _("{year} BC").format(year=-number)


class Game(models.Model):
    auth_token_hash  = models.CharField(max_length=200)
    create_date      = models.DateTimeField(auto_now_add=True)
    name             = models.CharField(max_length=200, unique=True)
    hostname         = models.CharField(max_length=200)
    port             = models.PositiveIntegerField(
        default=2056,
        validators=[MaxValueValidator(65535), MinValueValidator(1)]
    )
    manage_port      = models.PositiveIntegerField(
        default=13373,
        validators=[MaxValueValidator(65535), MinValueValidator(1)]
    )
    description      = models.TextField(blank=True, null=True)
    url              = models.CharField(max_length=200, blank=True, null=True)
    year             = models.SmallIntegerField(blank=True, null=True)
    turn             = models.PositiveSmallIntegerField(blank=True, null=True)
    # In hours
    turn_timer_max_h  = models.PositiveIntegerField(blank=True, null=True)
    # In seconds!
    turn_timer_left_s = models.PositiveIntegerField(blank=True, null=True)

    def turn_timer(self):
        return not self.turn_timer_max_h is None

    def year_str(self):
        return format_year(self.year)

    def __str__(self):
        return self.name


class Color():
    def __init__(self, rgbstr):
        darkness = 0
        try:
            rgb = self.rgbstr.split(',')
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
    id            = models.PositiveSmallIntegerField(primary_key=True)
    game          = models.ForeignKey(Game)
    name          = models.TextField(max_length=200)
    score         = models.PositiveIntegerField()
    finished_turn = models.BooleanField(default=False)
    # This is more like the status (e.g. AI, Offline)
    ping          = models.TextField(max_length=200, verbose_name='connection status')
    is_human      = models.BooleanField(default=False)
    is_claimed    = models.BooleanField(default=False)
    civilization  = models.TextField(max_length=200)
    leader        = models.TextField(max_length=200)
    # Formatted as "RRR,GGG,BBB" decimal
    color_rgb     = models.TextField(max_length=3 * 3 + 2)

    def color(self):
        return Color(self.color_rgb)


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
        return _("game was reloaded")


class GameLogServerTimeout(GameLog):
    def message(self):
        return _("server timed out")


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
        if self.increse:
            return _("Score increased to {score}").format(score=self.score)
        else:
            return _("Score decreased to {score}").format(score=self.score)


class GameLogNameChange(GameLogPlayer):
    player_name_new = models.CharField(max_length=200)

    def message(self):
        return _("Changed name to {new_name}").format(self.player_name_new)


class GameLogEliminated(GameLogPlayer):
    text = "Eliminated"


class GameLogAI(GameLogPlayer):
    text = "Converted to AI"


class GameLogClaimed(GameLogPlayer):
    text = "Claimed"


class StatusCache(models.Model):
    game = models.ForeignKey(Game)
    date = models.DateTimeField(db_index=True)
    json_status = models.TextField()
