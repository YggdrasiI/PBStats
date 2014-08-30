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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('auth_token_hash', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('hostname', models.CharField(max_length=200)),
                ('port', models.PositiveIntegerField(default=2056, validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateTimeField(db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameLogPlayer',
            fields=[
                ('gamelog_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLog', parent_link=True, primary_key=True, serialize=False)),
                ('player_name', models.CharField(max_length=200)),
                ('player_id', models.PositiveIntegerField(db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogNameChange',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLogPlayer', parent_link=True, primary_key=True, serialize=False)),
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
                ('gamelogplayer_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLogPlayer', parent_link=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogLogin',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLogPlayer', parent_link=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogFinish',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLogPlayer', parent_link=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogEliminated',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLogPlayer', parent_link=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogClaimed',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLogPlayer', parent_link=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogAI',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLogPlayer', parent_link=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogReload',
            fields=[
                ('gamelog_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLog', parent_link=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='GameLogScore',
            fields=[
                ('gamelogplayer_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLogPlayer', parent_link=True, primary_key=True, serialize=False)),
                ('score', models.PositiveIntegerField()),
                ('increase', models.BooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelogplayer',),
        ),
        migrations.CreateModel(
            name='GameLogTurn',
            fields=[
                ('gamelog_ptr', models.OneToOneField(auto_created=True, to='pbspy.GameLog', parent_link=True, primary_key=True, serialize=False)),
                ('year', models.SmallIntegerField()),
                ('turn', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('pbspy.gamelog',),
        ),
        migrations.CreateModel(
            name='StatusCache',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateTimeField(db_index=True)),
                ('json_status', models.TextField()),
                ('game', models.ForeignKey(to='pbspy.Game')),
            ],
            options={
            },
            bases=(models.Model,),
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
            field=models.ForeignKey(null=True, to='contenttypes.ContentType', related_name='polymorphic_pbspy.gamelog_set', editable=False),
            preserve_default=True,
        ),
    ]
