# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0012_auto_20141214_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
