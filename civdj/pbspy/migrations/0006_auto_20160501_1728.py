# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0005_auto_20160501_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='_victory_player_id',
            new_name='victory_player_id',
        ),
    ]
