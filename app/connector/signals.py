# signals.py

from django.conf import settings
from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def run_fetch_movie_data(sender, **kwargs):
    """
    Function to run a custom command after migrations are applied.
    """
    if settings.TEST:
        # Don't execute the signal during tests
        return
    else:
        call_command('fetch_movie_data')
