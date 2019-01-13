from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'civdj.views.home', name='home'),
    url(r'^admin/', admin.site.urls),
    # For now we simply redirect anything to pbspy!
    url(r'', include('pbspy.urls')),
]
