from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from connector.models import MoviesModel


class MoviesViewTestCase(APITestCase):
    URL_NAME_MOVIES = 'movies'

    def setUp(self):
        self.client = APIClient()
        self.movies_url = '/api/movies/'
        self.movies_url = self.api_url(self.URL_NAME_MOVIES, ['1'])

        self.movie = MoviesModel.objects.create(title='title')

    @classmethod
    def api_url(cls, view_name, args=None):
        url = reverse(view_name, args=args)
        return url

    def tearDown(self):
        # Clean up created objects
        MoviesModel.objects.all().delete()

    @patch('connector.views.MoviesOperations')
    @patch('connector.views.JWTStatelessUserAuthentication.authenticate')
    @patch('connector.views.permissions.IsAuthenticated.has_permission')
    def test_create_movie(
        self, mock_has_permission, mock_authenticate, MockMoviesOperations
    ):
        data = {'title': 'Test Movie', 'director': 'Test Director'}

        # Mocking the authenticate method to return a user object
        mock_authenticate.return_value = (None, None)

        # Mocking has_permission to always return True
        mock_has_permission.return_value = True

        # Mocking the create_movie_record method
        mock_create_movie_record = (
            MockMoviesOperations.return_value.create_movie_record
        )
        mock_create_movie_record.return_value = (
            None  # Mocking the method to return None
        )

        response = self.client.post(
            reverse(self.URL_NAME_MOVIES), data, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('connector.views.MoviesOperations')
    @patch('connector.views.JWTStatelessUserAuthentication.authenticate')
    @patch('connector.views.permissions.IsAuthenticated.has_permission')
    def test_partial_update_movie(
        self, mock_has_permission, mock_authenticate, MockMoviesOperations
    ):
        # Mocking the authenticate method to return a user object
        mock_authenticate.return_value = (None, None)

        # Mocking has_permission to always return True
        mock_has_permission.return_value = True

        # # Mocking the create_movie_record method
        mock_update_movie_record = (
            MockMoviesOperations.return_value.update_movie_record
        )
        mock_update_movie_record.return_value = (
            None  # Mocking the method to return None
        )

        data = {'director': 'Updated Director', 'title': 'title'}
        with patch(
            'connector.operations.MoviesOperations.get_movie_instance'
        ) as mock_get_movie:
            mock_get_movie.return_value = (
                None  # Mocking movie instance retrieval
            )
            response = self.client.put(self.movies_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('connector.views.JWTStatelessUserAuthentication.authenticate')
    @patch('connector.views.permissions.IsAuthenticated.has_permission')
    def test_retrieve_movie(self, mock_has_permission, mock_authenticate):
        # Mocking the authenticate method to return a user object
        mock_authenticate.return_value = (None, None)

        # Mocking has_permission to always return True
        mock_has_permission.return_value = True

        with patch(
            'connector.operations.MoviesOperations.get_movie_instance'
        ) as mock_get_movie:
            mock_get_movie.return_value = (
                None  # Mocking movie instance retrieval
            )
            response = self.client.get(self.movies_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('connector.views.JWTStatelessUserAuthentication.authenticate')
    @patch('connector.views.permissions.IsAuthenticated.has_permission')
    def test_list_movies(self, mock_has_permission, mock_authenticate):
        # Mocking the authenticate method to return a user object
        mock_authenticate.return_value = (None, None)

        # Mocking has_permission to always return True
        mock_has_permission.return_value = True

        url = reverse(self.URL_NAME_MOVIES)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('connector.views.JWTStatelessUserAuthentication.authenticate')
    @patch('connector.views.permissions.IsAuthenticated.has_permission')
    def test_delete_movie(self, mock_has_permission, mock_authenticate):
        # Mocking the authenticate method to return a user object
        mock_authenticate.return_value = (None, None)

        # Mocking has_permission to always return True
        mock_has_permission.return_value = True
        with patch(
            'connector.operations.MoviesOperations.get_movie_instance'
        ) as mock_get_movie:
            mock_get_movie.return_value = (
                self.movie
            )  # Mocking movie instance retrieval
            response = self.client.delete(self.movies_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
