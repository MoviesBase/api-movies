from django.core.management.base import BaseCommand

from connector.connectors import OMDBConnector
from connector.models import MoviesModel
from connector.serializers import MoviesSerializer


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not MoviesModel.objects.exists():
            movies_to_fetch = OMDBConnector().get_multiple_movies_by_title(
                pages=10, movie_title='horror'
            )

            # Save movies to the database
            if movies_to_fetch:
                serializer = MoviesSerializer(data=movies_to_fetch, many=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully fetched and saved movies to the database'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('No movies found from OMDB API')
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Database is not empty, skipping fetching movies'
                )
            )
