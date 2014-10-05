# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0002_auto_20140911_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='auth_token_hash',
        ),
        migrations.AlterField(
            model_name='game',
            name='url',
            field=models.CharField(max_length=200, blank=True, validators=[django.core.validators.URLValidator()], null=True),
        ),
    ]
