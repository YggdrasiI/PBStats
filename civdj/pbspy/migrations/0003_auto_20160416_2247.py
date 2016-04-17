# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0002_gamelogcurrenttimerchanged'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='victory_image',
            field=models.CharField(validators=[django.core.validators.URLValidator()], blank=True, null=True, max_length=200),
        ),
        migrations.AddField(
            model_name='game',
            name='victory_message',
            field=models.CharField(blank=True, null=True, max_length=2000),
        ),
    ]
