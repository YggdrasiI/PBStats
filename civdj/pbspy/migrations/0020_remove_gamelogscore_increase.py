# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0019_gamelogscore_increasetodelta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamelogscore',
            name='increase',
        ),
    ]
