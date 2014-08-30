# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0002_auto_20140830_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='manage_port',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)], default=13373),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='year',
            field=models.SmallIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
