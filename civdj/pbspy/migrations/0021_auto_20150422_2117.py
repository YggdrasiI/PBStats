# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0020_remove_gamelogscore_increase'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='mod_name',
            field=models.CharField(null=True, blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='gamelog',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_pbspy.gamelog_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
