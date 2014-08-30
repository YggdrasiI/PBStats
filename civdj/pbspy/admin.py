from django.contrib import admin
from pbspy.models import *

admin.site.register(Game)
admin.site.register(GameLog)
admin.site.register(GameLogLogin)
admin.site.register(GameLogTurn)
admin.site.register(StatusCache)
