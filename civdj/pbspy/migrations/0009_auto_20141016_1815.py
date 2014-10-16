# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0008_game_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelogmetachange',
            name='pb_name_old',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
