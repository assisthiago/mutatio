from datetime import datetime, time
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import models
from django.utils import timezone


class ReportManager(models.QuerySet):
    def from_today(self, *args, **kwargs):
        return self._filter(timezone.now(), **kwargs)

    def from_yesterday(self, *args, **kwargs):
        return self._filter(timezone.now() - timezone.timedelta(days=1), **kwargs)

    def last_availables(self, *args, **kwargs):
        if report := self.last():
            return self._filter(report.created_at, **kwargs)

        return None

    def _filter(self, period, *args, **kwargs):
        return self.filter(
            created_at__gte=datetime.combine(
                period, time.min, tzinfo=ZoneInfo(settings.TIME_ZONE)
            ),
            created_at__lte=datetime.combine(
                period, time.max, tzinfo=ZoneInfo(settings.TIME_ZONE)
            ),
            **kwargs,
        )
