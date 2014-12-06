# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0010_auto_20141201_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLogMissedTurn',
            fields=[
                ('gamelog_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pbspy.GameLog')),
                ('missed_turn_names', models.CharField(max_length=2000)),
                ('missed_turn_ids', models.CommaSeparatedIntegerField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
    ]
