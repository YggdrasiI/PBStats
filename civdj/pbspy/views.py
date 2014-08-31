from django.http import HttpResponseBadRequest, HttpResponse
from django.views import generic
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from pbspy.models import Game, GameLog, Player
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

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


@csrf_exempt
@require_http_methods(["POST"])
def game_update(request):
    try:
        game_id = int(request.POST['id'])
        pw_hash = request.POST['pwHash']
    except (KeyError, ValueError):
        return HttpResponseBadRequest('bad request')

    game = Game.objects.get(id=game_id)
    if pw_hash != game.auth_token_hash:
        return HttpResponse('unauthorized', status=401)  # Unauthorized

    try:
        info = json.loads(request.POST['info'])
    except (KeyError, ValueError):
        return HttpResponseBadRequest('bad request (info)')

    if info['return'] != 'ok':
        return HttpResponseBadRequest('bad request (return)')

    game.set_from_dict(info['info'])

    return HttpResponse('ok')