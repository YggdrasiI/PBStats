import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname is not None:
            try:
                timezone.activate(pytz.timezone(tzname))
            except pytz.exceptions.UnknownTimeZoneError:
# Print is not an option in middlewhere... where is this supposed to go?
#                print("Timezone error for tzname=", tzname)
                request.session['django_timezone'] = None
        else:
            timezone.activate(pytz.timezone('Europe/Berlin'))
