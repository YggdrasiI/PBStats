
from django import template
from datetime import datetime, timedelta
from django.utils import timezone

from django.utils import formats
from django.conf import settings

register = template.Library()


def log_date(value, arg):  # , date_now, distance_in_s):
        """Coarse displayed timestamp of old entries."""
        #now = datetime.now()  # wrong timezone offset
        now = timezone.now()
        delta = now - value
        if(delta.days >= arg):
            return formats.date_format(value, "SHORT_DATE_FORMAT")
        else:
            return formats.date_format(value, "SHORT_DATE_FORMAT") + ' ' + formats.date_format(value, "TIME_WITH_SECONDS_FORMAT")

register.filter('log_date', log_date)
