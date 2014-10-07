# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('auth_token_hash', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('hostname', models.CharField(max_length=200)),
                ('port', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)], default=2056)),
                ('manage_port', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)], default=13373)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.CharField(max_length=200, blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('is_paused', models.BooleanField(default=False)),
                ('year', models.FloatField(blank=True, null=True)),
                ('pb_name', models.CharField(max_length=200, blank=True, null=True)),
                ('turn', models.PositiveSmallIntegerField(default=0)),
                ('timer_max_h', models.PositiveIntegerField(blank=True, null=True)),
                ('timer_remaining_4s', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date', models.DateTimeField(db_index=True)),
                ('year', models.SmallIntegerField()),
                ('turn', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameLogMetaChange',
            fields=[
                ('gamelog_ptr', models.OneToOneField(to='pbspy.GameLog', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('pb_name_old', models.CharField(max_length=200)),
                ('pb_name', models.CharField(max_length=200)),
                ('player_count_old', models.SmallIntegerField()),
                ('player_count', models.SmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogPause',
            fields=[
                ('gamelog_ptr', models.OneToOneField(to='pbspy.GameLog', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('paused', models.BooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogPlayer',
            fields=[
                ('gamelog_ptr', models.OneToOneField(to='pbspy.GameLog', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('player_name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogNameChange',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(to='pbspy.GameLogPlayer', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('player_name_new', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogLogout',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(to='pbspy.GameLogPlayer', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogLogin',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(to='pbspy.GameLogPlayer', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogFinish',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(to='pbspy.GameLogPlayer', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogEliminated',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(to='pbspy.GameLogPlayer', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogClaimed',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(to='pbspy.GameLogPlayer', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogAI',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(to='pbspy.GameLogPlayer', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogReload',
            fields=[
                ('gamelog_ptr', models.OneToOneField(to='pbspy.GameLog', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogScore',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(to='pbspy.GameLogPlayer', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('score', models.PositiveIntegerField()),
                ('increase', models.BooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogServerTimeout',
            fields=[
                ('gamelog_ptr', models.OneToOneField(to='pbspy.GameLog', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogTimerChanged',
            fields=[
                ('gamelog_ptr', models.OneToOneField(to='pbspy.GameLog', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('timer_max_h', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogTurn',
            fields=[
                ('gamelog_ptr', models.OneToOneField(to='pbspy.GameLog', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ingame_id', models.PositiveSmallIntegerField()),
                ('name', models.TextField(max_length=200)),
                ('score', models.PositiveIntegerField()),
                ('finished_turn', models.BooleanField(default=False)),
                ('ping', models.TextField(max_length=200, verbose_name='connection status')),
                ('is_human', models.BooleanField(default=False)),
                ('is_claimed', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
                ('civilization', models.TextField(max_length=200)),
                ('leader', models.TextField(max_length=200)),
                ('color_rgb', models.TextField(max_length=11)),
                ('game', models.ForeignKey(to='pbspy.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('ingame_id', 'game')]),
        ),
        migrations.AlterIndexTogether(
            name='player',
            index_together=set([('ingame_id', 'game')]),
        ),
        migrations.AddField(
            model_name='gamelogplayer',
            name='player',
            field=models.ForeignKey(to='pbspy.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gamelog',
            name='game',
            field=models.ForeignKey(to='pbspy.Game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gamelog',
            name='polymorphic_ctype',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='polymorphic_pbspy.gamelog_set', editable=False),
            preserve_default=True,
        ),
    ]
