# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0003_auto_20140830_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamelogturn',
            name='turn',
        ),
        migrations.RemoveField(
            model_name='gamelogturn',
            name='year',
        ),
        migrations.AddField(
            model_name='gamelog',
            name='turn',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gamelog',
            name='year',
            field=models.SmallIntegerField(default=-2000),
            preserve_default=False,
        ),
    ]
