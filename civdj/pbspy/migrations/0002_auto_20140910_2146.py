# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pbspy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLogAdminAction',
            fields=[
                ('gamelog_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='pbspy.GameLog')),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogAdminEndTurn',
            fields=[
                ('gamelog_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='pbspy.GameLog')),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogAdminPause',
            fields=[
                ('gamelog_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='pbspy.GameLog')),
                ('paused', models.BooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogAdminSave',
            fields=[
                ('gamelogadminaction_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='pbspy.GameLogAdminAction')),
                ('filename', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogadminaction',),
        ),
        migrations.AddField(
            model_name='gamelogadminaction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='pb_remote_password',
            field=models.CharField(default='invalidpassword', max_length=200),
            preserve_default=False,
        ),
    ]
