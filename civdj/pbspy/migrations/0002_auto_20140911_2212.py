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
                ('gamelog_ptr', models.OneToOneField(serialize=False, to='pbspy.GameLog', primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogAdminEndTurn',
            fields=[
                ('gamelogadminaction_ptr', models.OneToOneField(serialize=False, to='pbspy.GameLogAdminAction', primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogadminaction',),
        ),
        migrations.CreateModel(
            name='GameLogAdminPause',
            fields=[
                ('gamelogadminaction_ptr', models.OneToOneField(serialize=False, to='pbspy.GameLogAdminAction', primary_key=True, auto_created=True, parent_link=True)),
                ('paused', models.BooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogadminaction',),
        ),
        migrations.CreateModel(
            name='GameLogAdminSave',
            fields=[
                ('gamelogadminaction_ptr', models.OneToOneField(serialize=False, to='pbspy.GameLogAdminAction', primary_key=True, auto_created=True, parent_link=True)),
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
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='pb_remote_password',
            field=models.CharField(default='invalidpassword', max_length=200),
            preserve_default=False,
        ),
    ]
