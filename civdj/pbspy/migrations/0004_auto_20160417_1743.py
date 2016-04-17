# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0003_auto_20160416_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='is_finished',
        ),
        migrations.AlterField(
            model_name='game',
            name='victory_image',
            field=models.CharField(null=True, max_length=200, blank=True, validators=[django.core.validators.URLValidator(regex='^.*[.](png|jpg|jpeg|git)$')]),
        ),
    ]
