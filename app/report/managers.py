from datetime import datetime, time, timedelta

from django.db import models


class ReportManager(models.QuerySet):
    def from_today(self, *args, **kwargs):
        return self._filter(datetime.today(), **kwargs)

    def from_yesterday(self, *args, **kwargs):
        return self._filter(datetime.today() - timedelta(days=1), **kwargs)

    def last_availables(self, *args, **kwargs):
        if report := self.last():
            return self._filter(report.created_at, **kwargs)

        return None

    def _filter(self, period, *args, **kwargs):
        return self.filter(
            created_at__gte=datetime.combine(period, time.min),
            created_at__lte=datetime.combine(period, time.max),
            **kwargs,
        )
