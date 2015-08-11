# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('pb_remote_password', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('hostname', models.CharField(max_length=200)),
                ('port', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)], default=2056)),
                ('manage_port', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)], default=13373)),
                ('description', models.TextField(null=True, blank=True)),
                ('url', models.CharField(validators=[django.core.validators.URLValidator()], null=True, max_length=200, blank=True)),
                ('last_update_successful', models.DateTimeField(null=True)),
                ('last_update_attempt', models.DateTimeField(default=datetime.datetime.now)),
                ('is_paused', models.BooleanField(default=False)),
                ('is_headless', models.BooleanField(default=False)),
                ('is_autostart', models.BooleanField(default=True)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('pb_name', models.CharField(null=True, max_length=200, blank=True)),
                ('mod_name', models.CharField(null=True, max_length=50, blank=True)),
                ('turn', models.PositiveSmallIntegerField(default=0)),
                ('timer_max_h', models.PositiveIntegerField(null=True, blank=True)),
                ('timer_remaining_4s', models.PositiveIntegerField(null=True, blank=True)),
                ('is_private', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('victory_player_id', models.SmallIntegerField(default=-1)),
                ('victory_type', models.SmallIntegerField(default=-1)),
                ('is_dynamic_ip', models.BooleanField(default=False)),
                ('admins', models.ManyToManyField(related_name='admin_games', to=settings.AUTH_USER_MODEL)),
                ('subscribed_users', models.ManyToManyField(related_name='subscribed_games', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameLog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateTimeField(db_index=True)),
                ('year', models.IntegerField()),
                ('turn', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('ingame_id', models.PositiveSmallIntegerField()),
                ('name', models.TextField(max_length=200)),
                ('score', models.PositiveIntegerField()),
                ('finished_turn', models.BooleanField(default=False)),
                ('ping', models.TextField(verbose_name='connection status', max_length=200)),
                ('is_human', models.BooleanField(default=False)),
                ('is_claimed', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
                ('civilization', models.TextField(max_length=200)),
                ('leader', models.TextField(max_length=200)),
                ('color_rgb', models.TextField(max_length=11)),
                ('game', models.ForeignKey(to='pbspy.Game')),
            ],
        ),
        migrations.CreateModel(
            name='GameLogAdminAction',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogForceDisconnect',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogMetaChange',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
                ('pb_name_old', models.CharField(null=True, max_length=200)),
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
            name='GameLogMissedTurn',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
                ('missed_turn_names', models.CharField(max_length=2000)),
                ('missed_turn_ids', models.CommaSeparatedIntegerField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogPause',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
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
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
                ('player_name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogReload',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogServerTimeout',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogTimerChanged',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
                ('timer_max_h', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogTurn',
            fields=[
                ('gamelog_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLog', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.AddField(
            model_name='gamelog',
            name='game',
            field=models.ForeignKey(to='pbspy.Game'),
        ),
        migrations.AddField(
            model_name='gamelog',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_pbspy.gamelog_set+', to='contenttypes.ContentType', null=True, editable=False),
        ),
        migrations.CreateModel(
            name='GameLogAdminEndTurn',
            fields=[
                ('gamelogadminaction_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogAdminAction', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogadminaction',),
        ),
        migrations.CreateModel(
            name='GameLogAdminPause',
            fields=[
                ('gamelogadminaction_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogAdminAction', serialize=False, auto_created=True, parent_link=True)),
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
                ('gamelogadminaction_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogAdminAction', serialize=False, auto_created=True, parent_link=True)),
                ('filename', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogadminaction',),
        ),
        migrations.CreateModel(
            name='GameLogAI',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogPlayer', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogClaimed',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogPlayer', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogEliminated',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogPlayer', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogFinish',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogPlayer', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogLogin',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogPlayer', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogLogout',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogPlayer', serialize=False, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogNameChange',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogPlayer', serialize=False, auto_created=True, parent_link=True)),
                ('player_name_new', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogScore',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(primary_key=True, to='pbspy.GameLogPlayer', serialize=False, auto_created=True, parent_link=True)),
                ('score', models.PositiveIntegerField()),
                ('delta', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
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
        ),
        migrations.AddField(
            model_name='gamelogadminaction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]
