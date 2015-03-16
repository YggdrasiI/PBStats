# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0017_auto_20150308_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamelogscore',
            name='delta',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
