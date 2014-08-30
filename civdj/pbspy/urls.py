from django.conf.urls import patterns, url

from pbspy import views

urlpatterns = patterns('',
    url(r'^$', views.game_list, name='game_list'),
    url(r'^game/(?P<pk>\d+)/$', views.game_detail, name='game_detail'),
    url(r'^game/(?P<game_id>\d+)/log/$', views.game_log, name='game_log'),
)