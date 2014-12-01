# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0009_auto_20141016_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='is_online',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='victory_player_id',
            field=models.SmallIntegerField(default=-1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='victory_type',
            field=models.SmallIntegerField(default=-1),
            preserve_default=True,
        ),
    ]
