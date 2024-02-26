import logging

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class OMDBConnector:
    def __init__(self):
        self.api_key = settings.OMDB_API_KEY
        self.url = 'http://www.omdbapi.com/'

    def get_movie_by_title(self, movie_title):
        try:
            response = requests.get(
                self.url,
                params={
                    'apikey': self.api_key,
                    'type': movie_title,
                    'r': 'json',
                    'page': 1,
                },
            )
            data = response.json()
            if data.get('Response') == 'True':
                movies = data.get('Search', [])

                return movies
            else:
                logger.exception('No movies found from OMDB API')
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)

    def get_multiple_movies_by_title(self, pages, movie_title):
        movies_from_omdb = []
        try:
            for page in range(1, pages + 1):
                response = requests.get(
                    self.url,
                    params={
                        'apikey': self.api_key,
                        's': movie_title,
                        'type': 'movie',
                        'r': 'json',
                        'page': page,
                    },
                )
                data = response.json()
                if data.get('Response') == 'True':
                    movies = data.get('Search', [])
                    movies_from_omdb.extend(movies)
                else:
                    logger.exception('No movies found from OMDB API')

            if movies_from_omdb:
                return movies_from_omdb
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)
