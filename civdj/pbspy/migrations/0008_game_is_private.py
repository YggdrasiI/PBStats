# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0007_gamelogforcedisconnect'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
