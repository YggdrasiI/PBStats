# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0006_auto_20141011_0211'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLogForceDisconnect',
            fields=[
                ('gamelog_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLog', primary_key=True, parent_link=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
    ]
