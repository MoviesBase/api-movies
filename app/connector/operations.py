import logging

from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException, NotFound

from connector import serializers
from connector.connectors import OMDBConnector
from connector.models import MoviesModel

logger = logging.getLogger(__name__)


class MoviesOperations:
    serializer_class = serializers.MoviesSerializer
    serializer_class_request = serializers.MovieRequestSerializer

    def create_movie_record(self, movie_title, context):
        """
        Creates Movie record in database
        movie_data: Movie title
        """
        try:
            movies_from_ombd = OMDBConnector().get_movie_by_title(
                movie_title.get('title')
            )
            serializer = self.serializer_class(
                data=movies_from_ombd, context=context, many=True
            )
        except MoviesModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)

        serializer.is_valid(raise_exception=True)
        serializer.save()

    def update_movie_record(self, movie_data, context, movie_instance):
        """
        Creates Movie record in database

        movie_data: Movie data
        context: {'contect':request}
        movie_instance: movie instance on given id
        """
        try:
            serializer = self.serializer_class(
                movie_instance, data=movie_data, context=context, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except MoviesModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)

    def get_movie_instance(self, movie_id):
        """
        Returns movie from the database on given ID
        Parameters: movie_id
        """
        try:
            movies = MoviesModel.objects.get(pk=movie_id)
            return movies
        except MoviesModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)

    def get_all_movies(self, page_size, title_filter=None):
        """
        Returns all the movies from the database
        Parameters: page_size
                    title_filter (optional)
        """
        try:
            queryset = MoviesModel.objects.all().order_by('title')
            if title_filter:
                queryset = queryset.filter(title__icontains=title_filter)
            return queryset[:page_size]
        except MoviesModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)

    def delete_movie_record(self, movie_instance):
        """
        Deletes Movie record in database
        Parameters: movie_instance  (movie instance on given id)
        """
        try:
            movie_instance.delete()
        except MoviesModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)
