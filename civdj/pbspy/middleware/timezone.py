import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            try:
                timezone.activate(pytz.timezone(tzname))
            except pytz.exceptions.UnknownTimeZoneError:
                request.session['django_timezone'] = None
        else:
            from django.conf import settings
            try:
                timezone.activate(pytz.timezone(settings.TIME_ZONE_INTERFACE))
            except AttributeError:
                timezone.deactivate()
        return self.get_response(request)
