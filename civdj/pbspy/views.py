from django.http import HttpResponseBadRequest, HttpResponse
from django.views import generic
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin

from pbspy.models import Game, GameLog
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

class GameListView(generic.ListView):
    model = Game

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

from pprint import pprint

@csrf_exempt
@require_http_methods(["POST"])
def game_update(request):
    print("INCOMING REQUEST")
    try:
        game_id = int(request.POST['id'])
        print(game_id)
        pw_hash = request.POST['pwHash']
        print(pw_hash)
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

    game.is_paused = info['bPaused']
    game.set_year(info['gameDate'])
    # TODO set turn
    game.pb_name = info['gameName']
    if info['turnTimer']:
        game.turn_timer_max_h  = info['turnTimerMax']
        game.turn_timer_left_s = info['turnTimerValue']
    else:
        game.turn_timer_max_h  = None
        game.turn_timer_left_s = None

    for player_info in info['players']:
        print(player_info['name'])
        # todo handle players

    game.save()

    return HttpResponse('1234')