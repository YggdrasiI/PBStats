# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
import operator
import functools
from datetime import datetime
import pytz
import logging

# from django import forms
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q, F
from django.db.models import Case, When
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.html import escape, strip_tags
from django.utils import timezone
from django.utils import formats

from pbspy.models import Game, GameLog, Player,\
        InvalidPBResponse, InvalidCharacterError
from pbspy.forms import GameForm, GameManagementChatForm, GameManagementMotDForm,\
        GameManagementTimerForm, GameManagementCurrentTimerForm, GameManagementLoadForm, GameManagementSetPlayerPasswordForm,\
        GameManagementSaveForm, GameLogTypesForm, GameLogSaveFilterForm, GameManagementShortNamesForm,\
        GameManagementSetPlayerColorForm, GameManagementSetVictoryForm

from pbspy.models import GameLogTurn, GameLogReload, GameLogMetaChange, GameLogTimerChanged,\
    GameLogPause, GameLogServerTimeout, GameLogPlayer, GameLogLogin, GameLogLogout,\
    GameLogFinish, GameLogScore, GameLogNameChange, GameLogEliminated, GameLogAI,\
    GameLogClaimed, GameLogAdminAction, GameLogAdminSave, GameLogAdminPause, GameLogAdminEndTurn,\
    GameLogForceDisconnect, GameLogMissedTurn, GameLogCurrentTimerChanged,\
    VictoryInfo


logger = logging.getLogger(__name__)


class GameListView(ListView):
    model = Game

    def get_queryset(self):
        # The year check filters out fake entries with have no connection
        # For public games, 'wrong_player_count' is duplicated for each admin due to the
        # necessary resulting left join with the game_admins table.
        # We can fix this by correcting after the fact even though it's really ugly
        games_queryset = self.model.objects.filter(
            Q(is_private=False) & ~Q(year=None) | Q(admins__id=self.request.user.id)
        ).annotate(
            wrong_player_count=Count(Case(When(player__ingame_stack=0, then=1))),
            admin_count=Count('admins__id', distinct=True)
        ).annotate(
            player_count=F('wrong_player_count')/F('admin_count')
        ).order_by('-id')

        self.refresh_games(games_queryset)
        return games_queryset

    @staticmethod
    def refresh_games(games_queryset):
        for game in games_queryset:
            game.refresh(300)


game_list = GameListView.as_view()


class GameDetailView(FormMixin, DetailView):
    model = Game
    form_class = GameLogTypesForm

    # List of possible orderings

    # Definitions of orderings
    player_orders = ['id', 'leader', 'score', 'civ', 'name', 'status', 'finished']
    # Note that minus sign just swap ordering of first key
    player_order_defs = {
        'id': ['ingame_id'],
        '-id': ['-ingame_id'],
        'leader': ['leader', '-score', 'ingame_id'],
        '-leader': ['-leader', '-score', 'ingame_id'],
        'score': ['-score', 'leader', 'ingame_id'],
        '-score': ['score', 'leader', 'ingame_id'],
        'civ': ['civilization', '-score', 'ingame_id'],
        '-civ': ['-civilization', '-score', 'ingame_id'],
        'name': ['name', '-score', 'ingame_id'],
        '-name': ['-name', '-score', 'ingame_id'],
        'status': ['ingame_id'],
        '-status': ['-ingame_id'],
        'finished': ['-finished_turn', '-score', 'ingame_id'],
        '-finished': ['finished_turn', '-score', 'ingame_id'],
    }

    # Tuple of GameLog sub classes (subset)
    log_classes = (
        GameLogFinish,
        GameLogLogin,
        GameLogLogout,
        GameLogScore,
        GameLogPause,
        GameLogTurn,
        GameLogReload,
        GameLogAI,
        GameLogClaimed,
        GameLogEliminated,
        GameLogNameChange,
        GameLogMissedTurn,
    )

    # Generate key and names for select form
    log_choices = tuple(
        [(l.__name__, l.generate_generic_log_type_name()()) for l in log_classes])
    log_keys = list(dict(log_choices).keys())

    player_choices = tuple(zip(range(52), range(52)))

    # Default offset for turn filtering of log
    # Note: Names confusing _min-value >= _max-value
    log_turn_filter = {'offset_max': 0, 'offset_min': 1}

    def player_list_setup(self, game, context):
        # 1. Get uri argument 'player_order'
        # Check if new value is allowed and overwrite
        # old session value.
        player_order_old = self.request.session.get('player_order', 'score')
        player_order_str = str(
            self.request.GET.get('player_order', player_order_old))
        if player_order_str != player_order_old:
            if player_order_str not in self.player_order_defs:
                player_order_str = player_order_old
            else:
                self.request.session['player_order'] = player_order_str

        # 2. Get list of keys which define the selected ordering
        player_order = self.player_order_defs.get(
            player_order_str,
            self.player_order_defs.get('score'))

        # 3. Create dict of the ordering keywords but add a
        #    minus sign for the current ordering.
        #    The dict can be used in templates to create links
        context['orders'] = dict(zip(self.player_orders, self.player_orders))
        if player_order_str in self.player_orders:
            context['orders'][player_order_str] = "-" + player_order_str
        context['orders']['current'] = player_order_str

        # 4. Attach ordered list of players
        context['players'] = list(
            game.player_set.filter(ingame_stack=0).order_by(*player_order))

        # 5. Post-processed sorting over properties without
        # simple sql definitions.
        if player_order_str == "status":
            context['players'] = sorted(
                context['players'], key=lambda pl: pl.status())
        if player_order_str == "-status":
            context['players'] = sorted(
                context['players'], key=lambda pl: pl.status(), reverse=True)

    def log_setup(self, game, context):
        # 0. Define turn filter
        turn_filter = self.request.session.get('log_turn_filter', GameDetailView.log_turn_filter)
        # Use absolute turn values to filter
        turn_max = game.turn - turn_filter['offset_max']
        turn_min = game.turn - turn_filter['offset_min']
        roundlog = game.gamelog_set.filter(Q(GameLog___turn__range=[turn_min, turn_max]))

        # 1. Define player filter
        player_id = int(self.request.GET.get('player_id', -1))
        if player_id > -1:
            self.request.session.setdefault('player_ids', {})[str(game.id)] = [player_id]
            self.request.session.modified = True

        player_ids = self.request.session.get('player_ids', {}).get(str(game.id), None)
        if player_ids is not None:
            p_list = [Q(**{'GameLogPlayer___player__id': None}),
                      Q(**{'GameLogPlayer___player__ingame_id__in': player_ids})
                      ]
        else:
            p_list = [Q()]
            player_ids = [-1]

        # 2. Define new form for log filter selection
        log_type_filter = self.request.session.get(
            'log_type_filter', GameDetailView.log_keys)
        log_filter_form = GameLogTypesForm()
        log_filter_form.fields['log_type_filter'].choices = GameDetailView.log_choices
        log_filter_form.fields['log_type_filter'].initial = log_type_filter
        log_filter_form.fields['log_turn_max'].initial = game.turn - turn_filter['offset_max']
        log_filter_form.fields['log_turn_min'].initial = game.turn - turn_filter['offset_min']
        log_filter_form.fields['log_player_ids'].choices = self.get_player_choices(game)
        log_filter_form.fields['log_player_ids'].initial = player_ids
        context['log_filter_form'] = log_filter_form

        # Form to save current filter
        filterstore = self.request.session.get('filterstore', {}).get(str(game.id),{})
        if len(filterstore) < GameLogSaveFilterForm.MAX_SAVEABLE_NUMBER:
            log_filter_save_form = GameLogSaveFilterForm()
            log_filter_save_form.fields['log_filter_name'].initial = ""
            context['log_filter_save_form'] = log_filter_save_form
        context['log_filter_save_list'] = filterstore

        # Just filter if not all types are selected
        if 0 < len(log_type_filter) < len(GameDetailView.log_choices):
            # Use A|B|... condition if less log types are selected
            # Otherwise use notA & notB & notC for the complement set
            c_list = []
            # This switch was disable because the result for
            # the else branch could be non-intuitive.
            #if len(log_type_filter) < 0.66 * len(GameDetailView.log_classes):
            if True:
                for c in GameDetailView.log_classes:
                    if c.__name__ in log_type_filter:
                        c_list.append(Q(**{'instance_of': c}))

                context['log'] = roundlog.filter(
                    functools.reduce(operator.or_, c_list)).filter(
                        functools.reduce(operator.or_, p_list)
                    ).order_by('-id')
            else:
                for c in GameDetailView.log_classes:
                    if c.__name__ not in log_type_filter:
                        c_list.append(Q(**{'not_instance_of': c}))

                context['log'] = roundlog.filter(
                    functools.reduce(operator.and_, c_list)).filter(
                        functools.reduce(operator.or_, p_list)
                    ).order_by('-id')
        else:
            context['log'] = roundlog.filter(
                functools.reduce(operator.or_, p_list)
            ).order_by('-id')

        # Remove log messages which should only readable for admins

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        game = self.object
        if not game.can_view(self.request.user):
            raise PermissionDenied()

        if self.request.GET.get('refresh'):
            game.refresh(30, True)
        else:
            game.refresh(30)

        context['can_manage'] = game.can_manage(self.request.user)

        # Player list
        self.player_list_setup(game, context)

        game.player_finished_count = \
            sum(1 for p in context['players'] if p.finished_turn)
        game.player_count = len(context['players'])

        self.log_setup(game, context)

        context['timezone'] = self.request.session.get('django_timezone')
        context['timezone_actual'] = timezone.get_current_timezone_name();
        if game.victory_type > -1:
            context['victory_info'] = VictoryInfo(game)
        return context

    @staticmethod
    def get_player_choices(game):
        # Generate list of (id,Name)-Tuples for formulars
        players_from_db = game.player_set.filter(ingame_stack=0).order_by('ingame_id')
        choices = [(p.ingame_id, "{:2}".format(p.ingame_id) + r"—" + p.name) for p in players_from_db]
        choices.insert(0, (-1, "All"))
        return tuple(choices)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        game = self.object
        if not game.can_view(self.request.user):
            raise PermissionDenied()

        form = GameLogTypesForm(request.POST)
        form.fields['log_type_filter'].choices = GameDetailView.log_choices
        form.fields['log_player_ids'].choices = self.get_player_choices(game)

        # FIXME what is up with this variable?
        # turn_filter = self.request.session.get('log_turn_filter', GameDetailView.log_turn_filter)

        if form.is_valid():
            # Save previous filter values
            save_current_filter(request.session, game, _("Previous"))

            log_type_filter = form.cleaned_data.get('log_type_filter')
            self.request.session['log_type_filter'] = log_type_filter
            self.request.session['log_turn_filter'] = {
                'offset_max': game.turn - form.cleaned_data.get('log_turn_max'),
                'offset_min': game.turn - form.cleaned_data.get('log_turn_min')
            }
            new_player_ids_str = form.cleaned_data.get('log_player_ids')
            new_player_ids = [int(pid) for pid in new_player_ids_str]
            if -1 in new_player_ids:
                new_player_ids = None

            # Note that subkeys of sessionvariables session will be converted
            # into str type. Thus, int(game.id) would be a bad choice as key.
            request.session.setdefault('player_ids', {})[str(game.id)] = new_player_ids
            request.session.modified = True
        else:
            return HttpResponseBadRequest('bad request')
            # return self.form_invalid(form)

        return HttpResponseRedirect(reverse('game_detail', args=[game.id]))


game_detail = GameDetailView.as_view()


class GameLogView(View,
                  MultipleObjectMixin,
                  MultipleObjectTemplateResponseMixin):
    model = GameLog
    template_name = "pbspy/game_log.html"

    def get(self, request, game_id):
        self.object_list = self.model.objects.filter(
            game_id__exact=game_id).order_by('-id')
        context = self.get_context_data()
        return self.render_to_response(context)


game_log = GameLogView.as_view()


@login_required()
def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST, user=request.user)
        if form.is_valid():
            game = form.save()
            game.admins.add(request.user)
            try:
                game.validate_connection()
                game.save()
                game.update()
                return HttpResponseRedirect(reverse('game_detail', args=[game.id]))
            except ValidationError:
                """
                TODO: The game creation allows to ping an arbitary server/port.
                    We should restrict the number of calls for each user.
                """
                # return HttpResponseBadRequest('Creation incomplete. PB server does not respond.')
                return HttpResponseRedirect(reverse('game_detail', args=[game.id]))
    else:
        form = GameForm(user=request.user)
    return render(request, 'pbspy/game_create.html', {'form': form})


def game_manage(request, game_id, action=""):
    game = Game.objects.get(id=game_id)
    if not game.can_manage(request.user):
        return HttpResponse('unauthorized', status=401)

    if not game.is_online:
        return HttpResponse('Can not manage. PB Server not available.', status=200)

    cur_timer_form = None
    if game.timer_remaining_4s is not None:
        cur_timer_form = GameManagementCurrentTimerForm( initial={
            'hours': int(game.timer_remaining_4s/4/3600),
            'minutes': int((game.timer_remaining_4s/4 % 3600)/60) })

    context = {'game': game,
               'timer_form': GameManagementTimerForm(initial={'timer': game.timer_max_h}),
               'current_timer_form': cur_timer_form,
               'chat_form': GameManagementChatForm(),
               'motd_form': GameManagementMotDForm(),
               'short_names_form': GameManagementShortNamesForm(),
               'save_form': GameManagementSaveForm()}

    saves = sorted(game.pb_list_saves(), key=lambda k: -k['timestamp'])
    load_choices = [('restart', 'Save and reload current game')]

    for save in saves:
        folder_index = int(save['folderIndex'])
        key = "/".join([str(folder_index), save['name']])
        label = "{} ({})".format(save['name'], save['date'])
        choice = (key, label)
        load_choices.append(choice)

    context['load_form'] = GameManagementLoadForm(load_choices)
    context['set_player_password_form'] = GameManagementSetPlayerPasswordForm(
        game.player_set.filter(ingame_stack=0))

    if request.method == 'POST':
        if action == 'pause_enable':
            game.pb_set_pause(True, user=request.user)
            return HttpResponse('pause enabled', status=200)
        elif action == 'pause_disable':
            game.pb_set_pause(False, user=request.user)
            return HttpResponse('pause disabled', status=200)
        elif action == 'headless_enable':
            game.pb_set_headless(True, user=request.user)
            return HttpResponse('headless mode enabled', status=200)
        elif action == 'headless_disable':
            game.pb_set_headless(False, user=request.user)
            return HttpResponse('headless mode disabled', status=200)
        elif action == 'autostart_enable':
            game.pb_set_autostart(True, user=request.user)
            return HttpResponse('pb autostart enabled', status=200)
        elif action == 'autostart_disable':
            game.pb_set_autostart(False, user=request.user)
            return HttpResponse('pb autostart disabled', status=200)
        elif action == 'remove_magellan_bonus':
            ret = game.pb_remove_magellan_bonus(1, user=request.user)
            return HttpResponse('Magellan bonus removed. Server returns: '
                                + ret['info'], status=200)
        elif action == 'prepare_mod_update':
            ret = game.pb_prepare_mod_update()
            return HttpResponse("Server returns: " + ret['info'] , status=200)
        elif action == 'end_turn':
            game.pb_end_turn(user=request.user)
            return HttpResponse('turn ended', status=200)
        elif action == 'set_current_turn_timer':
            form = GameManagementCurrentTimerForm(request.POST)
            if form.is_valid():
                game.pb_set_current_turn_timer(form.cleaned_data['hours'],
                                               form.cleaned_data['minutes'],
                                               20, user=request.user)
                return HttpResponse('timer set', status=200)
            context['current_timer_form'] = form
        elif action == 'set_turn_timer':
            form = GameManagementTimerForm(request.POST)
            if form.is_valid():
                game.pb_set_turn_timer(form.cleaned_data['timer'], user=request.user)
                return HttpResponse('timer set', status=200)
            context['timer_form'] = form
        elif action == 'chat':
            form = GameManagementChatForm(request.POST)
            if form.is_valid():
                ret = game.pb_chat(form.cleaned_data['message'], user=request.user)
                if ret["return"] == 'ok':
                    return HttpResponse("chat message '{0}' sent.".format(
                        ret['msg']), status=200)
                else:
                    return HttpResponse("Sending of chat message failed. "
                                        "Error: {0}.".format(
                                            ret['info']), status=200)
            context['chat_form'] = form
        elif action == 'motd':
            form = GameManagementMotDForm(request.POST)
            if form.is_valid():
                game.pb_set_motd(form.cleaned_data['message'], user=request.user)
                return HttpResponse('MotD sent.', status=200)
            context['motd_form'] = form
        elif action == 'short_names':
            form = GameManagementShortNamesForm(request.POST)
            if form.is_valid():
                game.pb_short_names(form.cleaned_data['iShortNameLen'],
                                    form.cleaned_data['iShortDescLen'],
                                    user=request.user)
                return HttpResponse('Set short names.', status=200)
            context['short_names_form'] = form
        elif action == 'save':
            form = GameManagementSaveForm(request.POST)
            if form.is_valid():
                try:
                    game.pb_save(form.cleaned_data['filename'],
                                 user=request.user)
                except InvalidCharacterError:
                    return HttpResponseBadRequest(
                        "The filename '{}' contains invalid characters!".format(
                            form.cleaned_data['filename']))
                else:
                    return HttpResponse('game saved.', status=200)
            context['save_form'] = form
        elif action == 'load':
            form = GameManagementLoadForm(load_choices, request.POST)
            if form.is_valid():
                selected_file = form.cleaned_data['filename']
                if selected_file == "restart":
                    game.pb_restart("", 0, user=request.user)
                else:
                    (folder_index_str, filename) = selected_file.split('/', 1)
                    folder_index = int(folder_index_str)
                    game.pb_restart(filename, folder_index, user=request.user)
                return HttpResponse('game loaded.', status=200)
            context['load_form'] = form
        elif action == 'set_player_password':
            form = GameManagementSetPlayerPasswordForm(
                game.player_set.filter(ingame_stack=0), request.POST)
            if form.is_valid():
                try:
                    game.pb_set_player_password(
                        form.cleaned_data['player'],
                        form.cleaned_data['password'],
                        user=request.user)
                    player = game.player_set.filter(ingame_stack=0).filter(id=form.cleaned_data['player'].id)[0]
                    return HttpResponse('Set password for player ' + str(player.ingame_id) + '/'
                                        + str(player.name) + '.', status=200)
                except InvalidPBResponse:
                    return HttpResponseBadRequest('Setting of password failed.')
            context['set_player_password_form'] = form
        elif action == 'set_player_color':
            form = GameManagementSetPlayerColorForm(
                game.player_set.filter(ingame_stack=0), int(request.POST['num_colors']), request.POST)
            if form.is_valid():
                game.pb_set_player_color(
                    form.cleaned_data['player'].ingame_id,
                    form.cleaned_data['color'],
                    user=request.user)
                context['set_color_message'] = form.cleaned_data['player'].name
                return render_game_manage_color(request, game, context)
            context['set_player_color_form'] = form
        elif action == 'kick':
            playerId = int(request.POST.get("id", -1))
            if playerId > -1:
                try:
                    game.pb_kick(playerId, user=request.user)
                    return HttpResponse('player kicked.', status=200)
                except InvalidPBResponse:
                    return HttpResponseBadRequest('Kicking of player %d failed.' % (playerId,))

            return HttpResponse('Cannot kick player. Wrong player id.', status=200)
        elif action == 'end_player_turn':
            playerId = int(request.POST.get("id", -1))
            if playerId > -1:
                try:
                    game.pb_end_player_turn(playerId, user=request.user)
                    return HttpResponse('player turn finished.', status=200)
                except InvalidPBResponse:
                    return HttpResponseBadRequest('Finishing turn of player %d failed.' % (playerId,))

            return HttpResponse('Cannot finish player turn. Wrong player id.', status=200)
        else:
            return HttpResponseBadRequest('bad request')

    context['action'] = action

    if action == 'color':
        return render_game_manage_color(request, game, context)
    elif action == 'load':
        return render_game_manage_load(request, game, context)
    elif action == 'kick':
        return render_game_manage_kick(request, game, context)
    elif action == 'end_player_turn':
        return render_game_manage_end_player_turn(request, game, context)
    elif action == 'motd':
        return render_game_manage_motd(request, game, context)

    return render(request, 'pbspy/game_manage.html', context)


def render_game_manage_color(request, game, context):
    context['colors'] = game.pb_list_colors()

    # Add RGB-Values as own list. (How to convert RGBA-Values in templates?!)
    def _rgb(rgba):
        rgb = [int(c) for c in rgba.split(",")][:3]
        #return ",".join([str(c) for c in rgb])
        return "#{0:02X}{1:02X}{2:02X}".format(*rgb)

    context['colorsRGB'] = [ {"id": rgba["id"],
                              "primary":_rgb(rgba["primary"]),
                              "secondary": _rgb(rgba["secondary"]),
                              "text": _rgb(rgba["text"])}
                            for rgba in context['colors']]

    if len(context['colors']) == 0:
        return HttpResponseBadRequest('Command not supported by PB Server.')
    context['set_player_color_form'] = GameManagementSetPlayerColorForm(
        game.player_set.filter(ingame_stack=0), len(context['colors']))
    return render(request, 'pbspy/game_manage_color.html', context)


def render_game_manage_victory(request, game, context):
    if 'set_game_victory_form' not in context:
        context['set_game_victory_form'] = GameManagementSetVictoryForm(instance=game)
        # Optional
        context['victory_info'] = VictoryInfo(game, True)
    return render(request, 'pbspy/game_manage_victory.html', context)


def render_game_manage_load(request, game, context):
    saves = sorted(game.pb_list_saves(), key=lambda k: -k['timestamp'])
    load_choices = [('restart', 'Save and reload current game')]

    for save in saves:
        folder_index = int(save['folderIndex'])
        key = "/".join([str(folder_index), save['name']])
        label = "{} ({})".format(save['name'], save['date'])
        choice = (key, label)
        load_choices.append(choice)

    context['load_form'] = GameManagementLoadForm(load_choices)
    context['players_online'] = game.get_online_players()
    return render(request, 'pbspy/game_manage_load.html', context)


def render_game_manage_kick(request, game, context):
    context['show_kick_table'] = True
    context['players'] = list(game.player_set.filter(ingame_stack=0).order_by('ingame_id'))
    context['players_online'] = game.get_online_players()
    return render(request, 'pbspy/game_manage_player_states.html', context)


def render_game_manage_end_player_turn(request, game, context):
    context['show_end_turn_table'] = True
    context['players'] = list(game.player_set.filter(ingame_stack=0).order_by('ingame_id'))
    context['players_online'] = game.get_online_players()
    return render(request, 'pbspy/game_manage_player_states.html', context)


def render_game_manage_motd(request, game, context):
    context['motd_form'] = GameManagementMotDForm()
    context['motd_form'].fields['message'].initial = game.pb_get_motd()
    return render(request, 'pbspy/game_manage_motd.html', context)


def set_timezone(request):
    #from django.conf import settings
    #tz =  str(request.COOKIES.get('timezone',settings.TIME_ZONE))
    tz = str(request.GET.get('timezone', request.COOKIES.get('timezone', None)))
    try:
        tzobj = pytz.timezone(tz)
    except pytz.exceptions.UnknownTimeZoneError:
        return HttpResponse('Invalid timezone: ' + escape(tz))

    request.session['django_timezone'] = tz
    return HttpResponse('Set timezone to ' + escape(tz), status=200)

def gen_browserconfig(request):
    return render(request, 'pbspy/browserconfig.xml', {})


@login_required()
def game_update_manual(request, game_id):
    game = Game.objects.get(id=game_id)
    game.update()
    return HttpResponse('ok', status=200)


@login_required()
def game_change(request, game_id, action=""):
    game = Game.objects.get(id=game_id)
    context = {'game': game}
    form = None

    if request.method == 'POST':
        if action == 'set_game_victory':
            form = GameManagementSetVictoryForm(request.POST, instance=game)
            if form.is_valid():
                form.save()
                context['victory_message_changed'] = True
                context['victory_info'] = VictoryInfo(game, True)
            context['set_game_victory_form'] = form
            return render_game_manage_victory(request, game, context)
        else:
            form = GameForm(request.POST, instance=game, user=request.user)
            if form.is_valid():
                form.save()
                try:
                    game.validate_connection()
                    game.update()
                    return HttpResponseRedirect(reverse('game_detail', args=[game.id]))
                except ValidationError:
                    # Form would still saved, but we will write a warning and display the form again.
                    context['game_no_connection'] = True
            else:
                context['game_data_not_valid'] = True

    if form is None:
        form = GameForm(instance=game, user=request.user)

    context['action'] = action

    if action == 'victory':
        return render_game_manage_victory(request, game, context)

    # Todo
    #game.pb_remote_password = GameForm.password_dummy

    # Add suggestion for valid json settings at Pitboss side
    context['json_settings'] = """
 [...]
 "webserver": {{
   "host": "",
   "password": "{pb_remote_password}",
   "port": {pb_manage_port}
  }},
 "webfrontend": {{
   "url": "{pbspy_url}",
   "sendPeriodicalData": 1,
   "gameId": {gameid},
   "sendInterval": 10
  }},
 [...]
 """.format(gameid=game.id,
            pbspy_url=r"http:\/\/"+request.get_host()+r"\/pbspy\/update",
            pb_remote_password=game.pb_remote_password,
            pb_manage_port=game.manage_port
           )

    context['form'] = form
    return render(request, 'pbspy/game_change.html', context)


@login_required()
@require_http_methods(['POST'])
def game_subscribe(request, game_id, subscribe=True):
    game = Game.objects.get(id=game_id)
    if subscribe:
        message = game.subscribe_user(request.user)
    else:
        message = game.unsubscribe_user(request.user)
    # TODO, also pass message... not sure how to do that easily ina redirect, probably ending up in a GET on a regex url
    return redirect('game_detail', pk=game_id)


@csrf_exempt
@require_http_methods(['POST'])
def game_update(request):
    try:
        game_id = int(request.POST['id'])
        pw_hash = request.POST['pwHash']
    except (KeyError, ValueError):
        logger.error('invalid game pw hash, id: {} / {}'.format(game_id, request.META.get('REMOTE_ADDR')))
        return HttpResponseBadRequest('bad request')
    except Game.DoesNotExist:
        logger.error('invalid game requested, id: {} / {}'.format(game_id, request.META.get('REMOTE_ADDR')))
        return HttpResponseBadRequest('game id not found')

    game = Game.objects.get(id=game_id)
    if pw_hash != game.auth_hash():
        return HttpResponse('unauthorized', status=401)

    if 'info' in request.POST:
        try:
            info = json.loads(request.POST['info'])
        except (KeyError, ValueError):
            return HttpResponseBadRequest('bad request (info)')

        if game.is_dynamic_ip:
            game.hostname = str(request.META.get("REMOTE_ADDR"))
            #game.save() # Not required. Should be redundant.

        if info['return'] != 'ok':
            return HttpResponseBadRequest('bad request (return)')
        game.set_from_dict(info['info'])
    elif 'force_disconnect' in request.POST:
        game.force_disconnect()
    else:
        return HttpResponseBadRequest('bad request (no idea what to do)')

    return HttpResponse('ok')


@require_http_methods(['POST'])
def game_save_filter(request, game_id):
    game = Game.objects.get(id=game_id)
    filterstore = request.session.setdefault('filterstore',{}).setdefault(str(game.id),{})
    form = GameLogSaveFilterForm(request.POST)

    if form.is_valid():
        filter_name = form.cleaned_data.get('log_filter_name','')
        filter_bAbsolute = form.cleaned_data.get(
            'log_filter_absolute_turns', False)
        if len(filter_name) == 0:
            date_joined = datetime.now()
            filter_name = formats.date_format(date_joined, "SHORT_DATETIME_FORMAT")
        save_current_filter(request.session, game, filter_name, filter_bAbsolute)

    return redirect('game_detail', pk=game_id)


def game_load_filter(request, game_id, filter_name=""):
    game = Game.objects.get(id=game_id)
    filterstore = request.session.get('filterstore', {}).get(str(game.id),{})
    if filterstore.get(filter_name) is None:
        return HttpResponse('No filter with this name found.', status=200)

    fd = filterstore.get(filter_name)
    if fd.get('bAbsolute', False):  # Interprets saved turns asbsolute values
        log_turn_filter = {
            'offset_max': game.turn - fd['turn_max'],
            'offset_min': game.turn - fd['turn_min'],
        }
    else:  # Hold the relative offset
        log_turn_filter = {
            'offset_max': fd.get('offset_max',
                                 game.turn - fd['turn_max']),
            'offset_min': fd.get('offset_min',
                                 game.turn - fd['turn_min']),
        }
    request.session.setdefault('player_ids', {})[str(game.id)] = fd['player_ids']
    request.session['log_turn_filter'] = log_turn_filter
    request.session['log_type_filter'] = fd['log_type_filter']
    request.session.modified = True

    return redirect('game_detail', pk=game_id)


def game_remove_filter(request, game_id, filter_name=""):
    game = Game.objects.get(id=game_id)
    filterstore = request.session.get('filterstore', {}).get(str(game.id),{})
    if filterstore.get(filter_name) is None:
        return HttpResponse('No filter with this name found.', status=200)

    filterstore.pop(filter_name)
    request.session.modified = True
    return redirect('game_detail', pk=game_id)


def save_default_filter(session, game):
    filter_name = _("Default")
    player_ids = None
    log_keys = GameDetailView.log_keys
    filter_definition = {
        'player_ids': player_ids,
        'turn_max': game.turn - 0,
        'turn_min': game.turn - 1,
        'offset_max': 0,
        'offset_min': 1,
        'bAbsolute': False,
        'log_type_filter': log_keys,
    }
    session.setdefault('filterstore',{}).setdefault(
        str(game.id),{})[filter_name] = filter_definition
    session.modified = True


def save_current_filter(session, game, filter_name, bAbsolute=False):
    filterstore = session.setdefault('filterstore',{}).setdefault(str(game.id),{})
    filter_name = str(filter_name)
    filter_name = escape(strip_tags(filter_name)).strip()
    m = GameLogSaveFilterForm.MAX_SAVEABLE_NUMBER
    if len(filterstore) >= m:
        raise ValueError(('Can not store more than %i entries.' % (m)))
    if len(filter_name) < 1:
        raise ValueError('Invalid filter name')

    player_ids = session.get('player_ids', {}).get(str(game.id), None)
    turn_filter = session.get('log_turn_filter', GameDetailView.log_turn_filter)
    log_keys = session.get('log_type_filter', GameDetailView.log_keys)
    filter_definition = {
        'player_ids': player_ids,
        'turn_max': game.turn - turn_filter['offset_max'],
        'turn_min': game.turn - turn_filter['offset_min'],
        'offset_max': turn_filter['offset_max'],
        'offset_min': turn_filter['offset_min'],
        'bAbsolute': bAbsolute,
        'log_type_filter': log_keys,
    }
    filterstore[filter_name] = filter_definition
    session.modified = True

    save_default_filter(session, game)
