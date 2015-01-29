# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0015_auto_20150113_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='update_date',
            new_name='last_update_successful',
        ),
        migrations.AlterField(
            model_name='game',
            name='last_update_attempt',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 19, 24, 1, 969950)),
        ),
    ]
