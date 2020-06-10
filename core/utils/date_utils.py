from django.utils import timezone


def increase_timedelta():
    return timezone.now() + timezone.timedelta(minutes=10)
