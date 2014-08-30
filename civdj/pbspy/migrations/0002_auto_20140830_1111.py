# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='url',
            field=models.CharField(blank=True, null=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
