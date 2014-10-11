# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0005_auto_20141005_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_autostart',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='is_headless',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
