# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0004_game_admins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='year',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gamelog',
            name='year',
            field=models.IntegerField(),
        ),
    ]
