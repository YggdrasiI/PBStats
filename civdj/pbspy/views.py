from django.http import HttpResponseBadRequest, HttpResponse
from django.views import generic
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from pbspy.models import Game, GameLog, Player, InvalidPBResponse
from pbspy.forms import GameForm, GameManagementChatForm, GameManagementMotDForm, GameManagementTimerForm,\
    GameManagementLoadForm, GameManagementSetPlayerPasswordForm, GameManagementSaveForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

import json


class GameListView(generic.ListView):
    model = Game

    def get_queryset(self):
        return self.model.objects.filter(Q(is_private=False) | Q(admins__id=self.request.user.id)).annotate(player_count=Count('player'))
#        return self.model.objects.annotate(player_count=Count('player'))

game_list = GameListView.as_view()


class GameDetailView(generic.DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        game = self.object
        if not game.can_view(self.request.user):
            raise PermissionDenied()

        context['can_manage'] = game.can_manage(self.request.user)
        context['players'] = list(game.player_set.all())
        context['log'] = game.gamelog_set.order_by('-id')
        return context

game_detail = GameDetailView.as_view()


class GameLogView(generic.View,
                  MultipleObjectMixin,
                  MultipleObjectTemplateResponseMixin):
    model = GameLog
    template_name = "pbspy/game_log.html"

    def get(self, request, game_id):
        self.object_list = self.model.objects.filter(game_id__exact=game_id).order_by('-id')
        context = self.get_context_data()
        return self.render_to_response(context)

game_log = GameLogView.as_view()
#
# def game_log(request, game_id):
#     log_entries = GameLog.objects.filter(game_id__exact=game_id).order_by('-id')[:30]
#     return HttpResponse("404")


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
    context['timer_form'] = GameManagementTimerForm(initial={'timer': game.timer_max_h})
    context['chat_form'] = GameManagementChatForm()
    context['motd_form'] = GameManagementMotDForm()
    context['save_form'] = GameManagementSaveForm()

    saves = sorted(game.pb_list_saves(), key=lambda k: -k['timestamp'])
    load_choices = []

    # Add entry for restart of running state
    load_choices.append( ('restart', 'Save and reload current game') )

    for save in saves:
        folderIndex = int(save['folderIndex'])
        key = "/".join([str(folderIndex), save['name']])
        label = "{} ({})".format(save['name'], save['date'])
        choice = (key, label)
        load_choices.append(choice)

    context['load_form'] = GameManagementLoadForm(load_choices)
    context['set_player_password_form'] = GameManagementSetPlayerPasswordForm(game.player_set)

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
                selectedFile = form.cleaned_data['filename']
                if selectedFile == "restart" :
                  game.pb_restart("", 0, request.user)
                else:
                  (folderIndex_str, filename) = selectedFile.split('/', 1)
                  folderIndex = int(folderIndex_str)
                  game.pb_restart(filename, folderIndex, request.user)
                return HttpResponse('game loaded.', status=200)
            context['load_form'] = form
        elif action == 'set_player_password':
            form = GameManagementSetPlayerPasswordForm(game.player_set, request.POST)
            if form.is_valid():
                game.pb_set_player_password(form.cleaned_data['player'].id, form.cleaned_data['password'])
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
