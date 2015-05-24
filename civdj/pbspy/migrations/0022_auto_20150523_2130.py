# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0021_auto_20150422_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_dynamic_ip',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='last_update_attempt',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='game',
            name='subscribed_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='subscribed_games', blank=True),
        ),
    ]
