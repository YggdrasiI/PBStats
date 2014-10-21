from django.http import HttpResponseBadRequest, HttpResponse
from django.views import generic
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from pbspy.models import Game, GameLog, Player, InvalidPBResponse
from pbspy.forms import GameForm, GameManagementChatForm, GameManagementMotDForm, GameManagementTimerForm,\
    GameManagementLoadForm, GameManagementSetPlayerPasswordForm, GameManagementSaveForm,\
    GameLogTypesForm

from pbspy.models import GameLogTurn, GameLogReload, GameLogMetaChange, GameLogTimerChanged,\
    GameLogPause, GameLogServerTimeout, GameLogPlayer, GameLogLogin, GameLogLogout,\
    GameLogFinish, GameLogScore, GameLogNameChange, GameLogEliminated, GameLogAI,\
    GameLogClaimed, GameLogAdminAction, GameLogAdminSave, GameLogAdminPause, GameLogAdminEndTurn,\
    GameLogForceDisconnect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

import json
import operator
import functools


class GameListView(generic.ListView):
    model = Game

    def get_queryset(self):
        return self.model.objects.filter(
            Q(is_private=False)
            | Q(admins__id=self.request.user.id)).annotate(
                player_count=Count('player', distinct=True))

game_list = GameListView.as_view()


class GameDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Game

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
        'finished': ['-finished_turn','ingame_id'],
        '-finished': ['finished_turn','ingame_id'],
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
    )

    # Generate key and names for select form
    log_choices = tuple(
        [(l.__name__, l.generateGenericLogTypeName()()) for l in log_classes])
    log_keys = dict(log_choices).keys()

    def player_list_setup(self, game, context):
        # 1. Get uri argument 'player_order'
        # Check if new value is allowed and overwrite
        # old session value.
        player_order_old = self.request.session.get('player_order', 'score')
        player_order_str = str(
            self.request.GET.get('player_order', player_order_old))
        if player_order_str != player_order_old:
            if not player_order_str in self.player_order_defs:
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
            game.player_set.all().order_by(*player_order))

        # 5. Post-processed sorting over properties without
        # simple sql definitions.
        if player_order_str == "status":
            context['players'] = sorted(
                context['players'], key=lambda pl: pl.status())
        if player_order_str == "-status":
            context['players'] = sorted(
                context['players'], key=lambda pl: pl.status(), reverse=True)

    def log_setup(self, game, context):
        # 1. Define player filter
        player_id = int(self.request.GET.get('player_id', -1))
        if player_id > -1:
            p_list = [Q(**{'GameLogPlayer___player__id': None}),
                      Q(**{'GameLogPlayer___player__id': player_id})]
        else:
            p_list = [Q()]

        # 2. Define new form for log filter selection
        log_filter = self.request.session.get(
            'log_filter', GameDetailView.log_keys)
        context['logFilterForm'] = GameLogTypesForm()
        context['logFilterForm'].fields[
            'log_filter'].choices = GameDetailView.log_choices
        context['logFilterForm'].fields['log_filter'].initial = log_filter
        context['logFilterForm'].fields['player_id'].initial = player_id

        # Just filter if not all types are selected
        if 0 < len(log_filter) < len(GameDetailView.log_choices):
            # Use A|B|... condition if less log types are selected
            # Otherwise use notA & notB & notC for the complement set
            c_list = []
            # This switch was disable because the result for
            # the else branch could be non-intuitive.
            #if len(log_filter) < 0.66 * len(GameDetailView.log_classes):
            if True:
                for c in GameDetailView.log_classes:
                    if c.__name__ in log_filter:
                        c_list.append(Q(**{'instance_of': c}))

                context['log'] = game.gamelog_set.filter(
                    functools.reduce(operator.or_, c_list)).filter(
                        functools.reduce(operator.or_, p_list)
                    ).order_by('-id')
            else:
                for c in GameDetailView.log_classes:
                    if not c.__name__ in log_filter:
                        c_list.append(Q(**{'not_instance_of': c}))

                context['log'] = game.gamelog_set.filter(
                    functools.reduce(operator.and_, c_list)).filter(
                        functools.reduce(operator.or_, p_list)
                    ).order_by('-id')
        else:
            context['log'] = game.gamelog_set.filter(
                functools.reduce(operator.or_, p_list)
            ).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        game = self.object
        if not game.can_view(self.request.user):
            raise PermissionDenied()

        context['can_manage'] = game.can_manage(self.request.user)

        # Player list
        self.player_list_setup(game, context)

        self.log_setup(game, context)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        game = self.object
        if not game.can_view(self.request.user):
            raise PermissionDenied()

        form = GameLogTypesForm(request.POST)
        form.fields['log_filter'].choices = GameDetailView.log_choices
        if form.is_valid():
            log_filter = form.cleaned_data.get('log_filter')
            self.request.session['log_filter'] = log_filter
        else:
            return HttpResponseBadRequest('bad request')
            # return self.form_invalid(form)

        return HttpResponseRedirect(reverse('game_detail', args=[game.id]))


game_detail = GameDetailView.as_view()


class GameLogView(generic.View,
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
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save()
            game.admins.add(request.user)
            game.save()
            game.update()
            return HttpResponseRedirect(reverse('game_detail', args=[game.id]))
    else:
        form = GameForm()
    return render(request, 'pbspy/game_create.html', {'form': form})


def game_manage(request, game_id, action=""):
    game = Game.objects.get(id=game_id)
    if not game.can_manage(request.user):
        return HttpResponse('unauthorized', status=401)

    context = {'game': game}
    context['timer_form'] = GameManagementTimerForm(
        initial={'timer': game.timer_max_h})
    context['chat_form'] = GameManagementChatForm()
    context['motd_form'] = GameManagementMotDForm()
    context['save_form'] = GameManagementSaveForm()

    saves = sorted(game.pb_list_saves(), key=lambda k: -k['timestamp'])
    load_choices = []

    # Add entry for restart of running state
    load_choices.append(('restart', 'Save and reload current game'))

    for save in saves:
        folder_index = int(save['folderIndex'])
        key = "/".join([str(folder_index), save['name']])
        label = "{} ({})".format(save['name'], save['date'])
        choice = (key, label)
        load_choices.append(choice)

    context['load_form'] = GameManagementLoadForm(load_choices)
    context['set_player_password_form'] = GameManagementSetPlayerPasswordForm(
        game.player_set)

    if request.method == 'POST':
        if action == 'pause_enable':
            game.pb_set_pause(True)
            return HttpResponse('pause enabled', status=200)
        elif action == 'pause_disable':
            game.pb_set_pause(False)
            return HttpResponse('pause disabled', status=200)
        elif action == 'headless_enable':
            game.pb_set_headless(True)
            return HttpResponse('headless mode enabled', status=200)
        elif action == 'headless_disable':
            game.pb_set_headless(False)
            return HttpResponse('headless mode disabled', status=200)
        elif action == 'autostart_enable':
            game.pb_set_autostart(True)
            return HttpResponse('pb autostart enabled', status=200)
        elif action == 'autostart_disable':
            game.pb_set_autostart(False)
            return HttpResponse('pb autostart disabled', status=200)
        elif action == 'end_turn':
            game.pb_end_turn()
            return HttpResponse('turn ended', status=200)
        elif action == 'set_turn_timer':
            form = GameManagementTimerForm(request.POST)
            if form.is_valid():
                game.pb_set_turn_timer(form.cleaned_data['timer'])
                return HttpResponse('timer set', status=200)
            context['timer_form'] = form
        elif action == 'chat':
            form = GameManagementChatForm(request.POST)
            if form.is_valid():
                game.pb_chat(form.cleaned_data['message'])
                return HttpResponse('chat message sent.', status=200)
            context['chat_form'] = form
        elif action == 'motd':
            form = GameManagementMotDForm(request.POST)
            if form.is_valid():
                game.pb_motd(form.cleaned_data['message'])
                return HttpResponse('MotD sent.', status=200)
            context['motd_form'] = form
        elif action == 'save':
            form = GameManagementSaveForm(request.POST)
            if form.is_valid():
                game.pb_save(form.cleaned_data['filename'], request.user)
                return HttpResponse('game saved.', status=200)
            context['save_form'] = form
        elif action == 'load':
            form = GameManagementLoadForm(load_choices, request.POST)
            if form.is_valid():
                selected_file = form.cleaned_data['filename']
                if selected_file == "restart":
                    game.pb_restart("", 0, request.user)
                else:
                    (folder_index_str, filename) = selected_file.split('/', 1)
                    folder_index = int(folder_index_str)
                    game.pb_restart(filename, folder_index, request.user)
                return HttpResponse('game loaded.', status=200)
            context['load_form'] = form
        elif action == 'set_player_password':
            form = GameManagementSetPlayerPasswordForm(
                game.player_set, request.POST)
            if form.is_valid():
                game.pb_set_player_password(
                    form.cleaned_data['player'].id,
                    form.cleaned_data['password'])
                return HttpResponse('passwort set.', status=200)
            context['set_player_password_form'] = form
        else:
            return HttpResponseBadRequest('bad request')

    context['action'] = action
    return render(request, 'pbspy/game_manage.html', context)


@login_required()
def game_update_manual(request, game_id):
    game = Game.objects.get(id=game_id)
    game.update()
    return HttpResponse('ok', status=200)


@csrf_exempt
@require_http_methods(["POST"])
def game_update(request):
    try:
        game_id = int(request.POST['id'])
        pw_hash = request.POST['pwHash']
    except (KeyError, ValueError):
        return HttpResponseBadRequest('bad request')

    game = Game.objects.get(id=game_id)
    if pw_hash != game.auth_hash():
        return HttpResponse('unauthorized', status=401)

    if 'info' in request.POST:
        try:
            info = json.loads(request.POST['info'])
        except (KeyError, ValueError):
            return HttpResponseBadRequest('bad request (info)')
        if info['return'] != 'ok':
            return HttpResponseBadRequest('bad request (return)')
        game.set_from_dict(info['info'])
    elif 'force_disconnect' in request.POST:
        game.force_disconnect()
    else:
        return HttpResponseBadRequest('bad request (no idea what to do)')

    return HttpResponse('ok')
