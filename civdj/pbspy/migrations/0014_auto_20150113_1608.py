# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0013_auto_20150110_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 16, 8, 8, 412919)),
        ),
    ]
