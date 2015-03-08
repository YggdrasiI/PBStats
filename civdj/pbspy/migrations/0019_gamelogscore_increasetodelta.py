# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def increase_to_delta(apps, schema_editor):
    game_log_score_class = apps.get_model("pbspy", "GameLogScore")
    player_class = apps.get_model("pbspy", "Player")
    for player in player_class.objects.all():
        previous_score = 0
        for gls in game_log_score_class.objects.all().filter(player=player).order_by('date'):
            gls.delta = gls.score - previous_score
            if (gls.increase and gls.delta <= 0) or (not gls.increase and gls.delta >= 0):
                print("Bogus log conversion: {player} {date} {inde} {delta:+} -> {score}".format(
                    player=player, inde="increased" if gls.increase else "decreased",
                    delta=gls.delta, score=gls.score, date=gls.date))

            previous_score = gls.score
            gls.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0018_gamelogscore_delta'),
    ]

    operations = [
        migrations.RunPython(increase_to_delta),
    ]
