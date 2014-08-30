# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbspy', '0005_gamelogservertimeout'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.PositiveSmallIntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField(max_length=200)),
                ('score', models.PositiveIntegerField()),
                ('finished_turn', models.BooleanField(default=False)),
                ('ping', models.TextField(verbose_name='connection status', max_length=200)),
                ('is_human', models.BooleanField(default=False)),
                ('is_claimed', models.BooleanField(default=False)),
                ('civilization', models.TextField(max_length=200)),
                ('leader', models.TextField(max_length=200)),
                ('color', models.TextField(max_length=11)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='game',
            name='turn_timer_left_s',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='turn_timer_max_h',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
