from django.db import models
from django.utils import timezone
from datetime import timedelta


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        now = timezone.now()

        leaved_at = self.leaved_at if self.leaved_at else now
        return leaved_at - self.entered_at

    def is_long(self, minutes=60):
        duration = self.get_duration()
        return duration > timedelta(minutes=minutes)


def format_duration(duration):

    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)

    minutes, seconds = divmod(remainder, 60)
    return f'{hours}ч {minutes}мин'
