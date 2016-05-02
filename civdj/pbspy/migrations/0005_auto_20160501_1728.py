# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0004_auto_20160417_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='victory_player_id',
        ),
        migrations.AddField(
            model_name='game',
            name='_victory_player_id',
            field=models.OneToOneField(null=True, to='pbspy.Player', blank=True, related_name='+'),
        ),
    ]
