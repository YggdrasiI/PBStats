# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLogCurrentTimerChanged',
            fields=[
                ('gamelog_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='pbspy.GameLog', on_delete=models.CASCADE, primary_key=True, serialize=False)),
                ('from_4s', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('to_4s', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
    ]
