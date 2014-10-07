from django.http import HttpResponseBadRequest, HttpResponse
from django.views import generic
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from pbspy.models import Game, GameLog, Player
from pbspy.forms import GameForm, GameManagementChatForm, GameManagementTimerForm, GameManagementLoadForm, \
    GameManagementSetPlayerPasswordForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import json


class GameListView(generic.ListView):
    model = Game

    def get_queryset(self):
        return self.model.objects.annotate(player_count=Count('player'))

game_list = GameListView.as_view()


class GameDetailView(generic.DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        game = self.object
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

    if request.method == 'POST':
        if action == 'pause_enable':
            game.pb_set_pause(True)
        elif action == 'pause_disable':
            game.pb_set_pause(False)
        elif action == 'set_turn_timer':
            form = GameManagementTimerForm(request.POST)
            if not form.is_valid():
                return HttpResponseBadRequest('invalid form')
            game.pb_set_turn_timer(form.timer)
        elif action == 'end_turn':
            game.pb_end_turn()
        elif action == 'chat':
            form = GameManagementChatForm(request.POST)
            if not form.is_valid():
                return HttpResponseBadRequest('invalid form')
            game.pb_chat(form.message)
        else:
            return HttpResponseBadRequest('bad request')

    context = {'game': game}
    context['timer_form'] = GameManagementTimerForm(initial={'timer': game.timer_max_h})
    context['chat_form'] = GameManagementChatForm()
    saves = sorted(game.pb_list_saves(), key=lambda k: -k['timestamp'])
    load_choices = [(save['name'], "{} ({})".format(save['name'], save['date']))
                    for save in saves]
    context['load_form'] = GameManagementLoadForm(load_choices)
    context['set_player_password_form'] = GameManagementSetPlayerPasswordForm(game.player_set)
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

    try:
        info = json.loads(request.POST['info'])
    except (KeyError, ValueError):
        return HttpResponseBadRequest('bad request (info)')

    if info['return'] != 'ok':
        return HttpResponseBadRequest('bad request (return)')

    game.set_from_dict(info['info'])

    return HttpResponse('ok')