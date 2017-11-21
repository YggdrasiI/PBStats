# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0006_auto_20160501_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='ingame_stack',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('ingame_id', 'game', 'ingame_stack')]),
        ),
    ]
