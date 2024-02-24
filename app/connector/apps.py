import time

from django.apps import AppConfig
from django.core import management
from django.db import connection
from django.db.utils import OperationalError


class ConnectorConfig(AppConfig):
    name = 'connector'

    def ready(self):
        # Attempt to establish a database connection
        establish_database_connection()

        # Call the management command after database connection is established
        management.call_command('fetch_movie_data')


def establish_database_connection():
    """
    Attempts to establish a database connection.
    Raises OperationalError if the maximum number of tries is reached.
    """
    max_tries = 5

    tries = 0
    while tries <= max_tries:
        try:
            # Try to establish a database connection
            connection.ensure_connection()
            return  # Exit the function if connection is successful
        except OperationalError:
            # If connection fails,
            # wait for a short interval before trying again
            time.sleep(1)
            tries += 1

    # If maximum number of attempts reached, raise an exception
    raise OperationalError(
        'Failed to establish a database connection after {} attempts'.format(
            max_tries
        )
    )
