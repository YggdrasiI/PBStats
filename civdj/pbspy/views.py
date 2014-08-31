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

    info = info['info']  # ?!

    game.pb_name   = info['gameName']
    game.turn      = info['gameTurn']
    game.is_paused = info['bPaused']
    game.set_year(info['gameDate'])

    if info['turnTimer']:
        game.turn_timer_max_h  = info['turnTimerMax']
        game.turn_timer_left_s = info['turnTimerValue']
    else:
        game.turn_timer_max_h  = None
        game.turn_timer_left_s = None

    for player_info in info['players']:
        try:
            player = game.player_set.get(ingame_id=player_info['id'])
        except Player.DoesNotExist:
            player = Player(ingame_id=player_info['id'], game=game)
        player.finished_turn = player_info['finishedTurn']
        player.name          = player_info['name']
        player.score         = int(player_info['score'])
        player.ping          = player_info['ping']
        player.is_human      = player_info['bHuman']
        player.is_claimed    = player_info['bClaimed']
        player.civilization  = player_info['civilization']
        player.leader        = player_info['leader']
        player.color         = player_info['color']
        player.save()

    game.save()

    return HttpResponse('ok')