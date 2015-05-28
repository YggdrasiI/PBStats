# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0020_remove_gamelogscore_increase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='last_update_attempt',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
