
from django import template
from datetime import datetime, timedelta
from django.utils import timezone

from django.utils import formats
from django.conf import settings

register = template.Library()


def log_date(value, threshold_days):  # , date_now, distance_in_s):
        """Removes time from datetimes older than threshold_days days."""
        # Do not use datetime.now() as this is a
        now = timezone.now()
        delta = now - value
        if delta.days >= threshold_days:
            return formats.date_format(value, "SHORT_DATE_FORMAT")
        else:
            return (formats.date_format(value, "SHORT_DATE_FORMAT") + ' ' +
                    formats.date_format(value, "TIME_WITH_SECONDS_FORMAT"))

register.filter('log_date', log_date)
