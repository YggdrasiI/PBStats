from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'civdj.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    # For now we simply redirect anything to pbspy!
    url(r'', include('pbspy.urls')),
)
