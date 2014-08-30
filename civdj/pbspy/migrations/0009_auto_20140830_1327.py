# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0008_delete_test'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='color',
            new_name='color_rgb',
        ),
        migrations.RemoveField(
            model_name='gamelogplayer',
            name='player_id',
        ),
        migrations.AddField(
            model_name='gamelogplayer',
            name='player',
            field=models.ForeignKey(default=None, to='pbspy.Player'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ForeignKey(default=0, to='pbspy.Game'),
            preserve_default=False,
        ),
    ]
