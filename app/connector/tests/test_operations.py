from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework.exceptions import APIException, NotFound, ValidationError

from connector.models import MoviesModel
from connector.operations import MoviesOperations


class MoviesOperationsTest(TestCase):
    def setUp(self):
        self.movies_operations = MoviesOperations()

    def tearDown(self):
        # Clean up created objects
        MoviesModel.objects.all().delete()

    @patch('connector.operations.OMDBConnector.get_movie_by_title')
    def test_create_movie_record(self, mock_get_movie_by_title):
        mock_get_movie_by_title.return_value = [{'Title': 'Test Movie'}]

        context = {'request': MagicMock()}
        self.movies_operations.create_movie_record(
            {'title': 'Test Movie'}, context
        )

        self.assertTrue(
            MoviesModel.objects.filter(title='Test Movie').exists()
        )

    @patch('connector.operations.OMDBConnector.get_movie_by_title')
    def test_create_movie_record_empty_title(self, mock_get_movie_by_title):
        context = {'request': MagicMock()}
        with self.assertRaises(ValidationError):
            self.movies_operations.create_movie_record({'title': ''}, context)

    @patch('connector.operations.OMDBConnector.get_movie_by_title')
    def test_create_movie_record_non_existent_title(
        self, mock_get_movie_by_title
    ):
        mock_get_movie_by_title.return_value = None

        context = {'request': MagicMock()}
        with self.assertRaises(NotFound):
            self.movies_operations.create_movie_record(
                {'title': 'Non Existent Movie'}, context
            )

    @patch('connector.operations.OMDBConnector.get_movie_by_title')
    def test_create_movie_record_invalid_data_returned(
        self, mock_get_movie_by_title
    ):
        mock_get_movie_by_title.return_value = [{'InvalidKey': 'Test Movie'}]

        context = {'request': MagicMock()}
        with self.assertRaises(ValidationError):
            self.movies_operations.create_movie_record(
                {'title': 'Test Movie'}, context
            )

    @patch('connector.operations.OMDBConnector.get_movie_by_title')
    def test_create_movie_record_duplicate_title(
        self, mock_get_movie_by_title
    ):
        MoviesModel.objects.create(title='Test Movie')

        mock_get_movie_by_title.return_value = [{'Title': 'Test Movie'}]

        context = {'request': MagicMock()}
        with self.assertRaises(ValidationError):
            self.movies_operations.create_movie_record(
                {'title': 'Test Movie'}, context
            )

    @patch('connector.operations.OMDBConnector.get_movie_by_title')
    def test_create_movie_record_api_exception(self, mock_get_movie_by_title):
        mock_get_movie_by_title.side_effect = APIException('API Error')

        context = {'request': MagicMock()}
        with self.assertRaises(APIException):
            self.movies_operations.create_movie_record(
                {'title': 'Test Movie'}, context
            )

    @patch('connector.operations.MoviesModel.objects.get')
    def test_get_movie_instance(self, mock_get):
        mock_movie_instance = MagicMock()
        mock_get.return_value = mock_movie_instance

        movie_instance = self.movies_operations.get_movie_instance(1)

        self.assertEqual(movie_instance, mock_movie_instance)

    def test_get_movie_instance_non_existent_id(self):
        with self.assertRaises(NotFound):
            self.movies_operations.get_movie_instance(9999)

    def test_get_movie_instance_invalid_id_format(self):
        with self.assertRaises(ValueError):
            self.movies_operations.get_movie_instance('invalid_id')

    @patch('connector.operations.MoviesModel.objects.get')
    def test_get_movie_instance_api_exception(self, mock_get):
        mock_get.side_effect = APIException('API Error')

        with self.assertRaises(APIException):
            self.movies_operations.get_movie_instance(1)

    @patch('connector.operations.MoviesModel.objects.get')
    def test_get_movie_instance_deleted_movie(self, mock_get):
        mock_get.side_effect = MoviesModel.DoesNotExist()

        with self.assertRaises(NotFound):
            self.movies_operations.get_movie_instance(1)

    @patch('connector.operations.MoviesModel.objects.get')
    def test_get_movie_instance_multiple_instances_same_id(self, mock_get):
        mock_get.side_effect = MoviesModel.MultipleObjectsReturned()

        with self.assertRaises(ValidationError):
            self.movies_operations.get_movie_instance(1)

    def test_get_all_movies(self):
        MoviesModel.objects.create(title='Test Movie 1')
        MoviesModel.objects.create(title='Test Movie 2')

        movies = self.movies_operations.get_all_movies(page_size=2)

        self.assertEqual(len(movies), 2)
        self.assertEqual(movies[0].title, 'Test Movie 1')
        self.assertEqual(movies[1].title, 'Test Movie 2')

    def test_get_all_movies_no_movies_in_database(self):
        movies = self.movies_operations.get_all_movies(page_size=10)
        self.assertEqual(len(movies), 0)

    def test_get_all_movies_limited_page_size(self):
        MoviesModel.objects.create(title='Test Movie 1')
        MoviesModel.objects.create(title='Test Movie 2')

        movies = self.movies_operations.get_all_movies(page_size=1)
        self.assertEqual(len(movies), 1)

    def test_get_all_movies_invalid_title_filter(self):
        MoviesModel.objects.create(title='Test Movie 1')
        MoviesModel.objects.create(title='Test Movie 2')

        movies = self.movies_operations.get_all_movies(
            page_size=10, title_filter='Non-existent'
        )
        self.assertEqual(len(movies), 0)

    @patch('connector.operations.MoviesModel.objects.all')
    def test_get_all_movies_api_exception(self, mock_all):
        mock_all.side_effect = APIException('API Error')

        with self.assertRaises(APIException):
            self.movies_operations.get_all_movies(page_size=10)

    @patch('connector.operations.MoviesModel.objects.get')
    def test_update_movie_record(self, mock_get):
        mock_movie_instance = MagicMock()
        mock_get.return_value = mock_movie_instance

        context = {'request': MagicMock()}
        self.movies_operations.update_movie_record(
            {}, context, movie_instance=mock_movie_instance
        )

        mock_movie_instance.save.assert_called_once()

    def test_update_movie_record_invalid_movie_data(self):
        movie_instance = MoviesModel.objects.create(title='Test Movie')
        context = {'request': MagicMock()}

        with self.assertRaises(ValidationError):
            self.movies_operations.update_movie_record(
                {}, context, movie_instance
            )

    def test_update_movie_record_non_existent_instance(self):
        context = {'request': MagicMock()}

        with self.assertRaises(NotFound):
            self.movies_operations.update_movie_record(
                {}, context, movie_instance=None
            )

    def test_update_movie_record_partial_update_valid_data(self):
        movie_instance = MoviesModel.objects.create(title='Test Movie')
        context = {'request': MagicMock()}

        self.movies_operations.update_movie_record(
            {'title': 'Updated Title'}, context, movie_instance
        )
        updated_movie = MoviesModel.objects.get(pk=movie_instance.pk)
        self.assertEqual(updated_movie.title, 'Updated Title')

    def test_update_movie_record_full_update_valid_data(self):
        movie_instance = MoviesModel.objects.create(title='Test Movie')
        context = {'request': MagicMock()}

        self.movies_operations.update_movie_record(
            {'title': 'Updated Title', 'genre': 'Comedy'},
            context,
            movie_instance,
        )
        updated_movie = MoviesModel.objects.get(pk=movie_instance.pk)
        self.assertEqual(updated_movie.title, 'Updated Title')
        self.assertEqual(updated_movie.genre, 'Comedy')

    @patch('connector.operations.MoviesModel.objects.get')
    def test_update_movie_record_api_exception(self, mock_get):
        mock_get.side_effect = APIException('API Error')
        context = {'request': MagicMock()}

        with self.assertRaises(APIException):
            self.movies_operations.update_movie_record(
                {'title': 'Updated Title'},
                context,
                movie_instance=MoviesModel(),
            )

    @patch('connector.operations.MoviesModel.objects.get')
    def test_delete_movie_record(self, mock_get):
        mock_movie_instance = MagicMock()
        mock_get.return_value = mock_movie_instance

        self.movies_operations.delete_movie_record(
            movie_instance=mock_movie_instance
        )

        mock_movie_instance.delete.assert_called_once()

    def test_delete_movie_record_non_existent_instance(self):
        with self.assertRaises(NotFound):
            self.movies_operations.delete_movie_record(movie_instance=None)

    def test_delete_movie_record_success(self):
        movie_instance = MoviesModel.objects.create(title='Test Movie')

        self.movies_operations.delete_movie_record(
            movie_instance=movie_instance
        )
        self.assertFalse(
            MoviesModel.objects.filter(pk=movie_instance.pk).exists()
        )

    @patch('connector.operations.MoviesModel.objects.get')
    def test_delete_movie_record_api_exception(self, mock_get):
        mock_get.side_effect = APIException('API Error')

        with self.assertRaises(APIException):
            self.movies_operations.delete_movie_record(
                movie_instance=MoviesModel()
            )
