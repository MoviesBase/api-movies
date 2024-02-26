# signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command


@receiver(post_migrate)
def run_fetch_movie_data(sender, **kwargs):
    """
    Function to run a custom command after migrations are applied.
    """
    call_command('fetch_movie_data')
