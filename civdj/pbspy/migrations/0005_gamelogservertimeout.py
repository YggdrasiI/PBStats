# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0004_auto_20140830_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLogServerTimeout',
            fields=[
                ('gamelog_ptr', models.OneToOneField(to='pbspy.GameLog', parent_link=True, auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
    ]
