import pytz

from django.utils import timezone

class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname != None:
            try:
              timezone.activate(pytz.timezone(tzname))
            except pytz.exceptions.UnknownTimeZoneError as e:
                print "Timezone error for tzname=", tzname
                request.session['django_timezone'] = None
        else:
            timezone.deactivate()
