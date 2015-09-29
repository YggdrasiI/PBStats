
from django import template
from datetime import datetime, timedelta
from django.utils import timezone

from django.utils import formats
from django.conf import settings

register = template.Library()

@register.filter(expects_localtime=True)
def log_date_privacy(log_date, threshold_days):
    """Removes time from datetimes older than threshold_days days."""
    now = timezone.now()
    delta = now - log_date
    if delta.days >= threshold_days:
        return formats.date_format(log_date, "SHORT_DATE_FORMAT")
    else:
        return (formats.date_format(log_date, "SHORT_DATE_FORMAT") + ' ' +
                formats.time_format(log_date, "TIME_WITH_SECONDS_FORMAT"))


@register.filter(expects_localtime=True)
def log_player_privacy(logentry, theshold_days):
    now = timezone.now()
    delta = now - logentry.date
    try:
        if delta.days >= theshold_days:
            return logentry.player.leader
        else:
            return logentry.player_name
    except AttributeError:
        return '-'
