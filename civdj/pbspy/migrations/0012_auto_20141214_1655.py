# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pbspy', '0011_gamelogmissedturn'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='subscribed_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='subscribed_games'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='admins',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='admin_games'),
        ),
    ]
