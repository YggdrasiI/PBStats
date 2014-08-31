from django.contrib import admin
from pbspy.models import *

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(GameLog)
admin.site.register(GameLogAI)
admin.site.register(GameLogClaimed)
admin.site.register(GameLogEliminated)
admin.site.register(GameLogFinish)
admin.site.register(GameLogLogin)
admin.site.register(GameLogLogout)
admin.site.register(GameLogNameChange)
admin.site.register(GameLogPlayer)
admin.site.register(GameLogReload)
admin.site.register(GameLogScore)
admin.site.register(GameLogServerTimeout)
admin.site.register(GameLogTurn)
admin.site.register(StatusCache)
