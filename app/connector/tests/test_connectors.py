from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework.exceptions import APIException, NotFound

from connector.connectors import OMDBConnector


class OMDBConnectorTest(TestCase):
    @patch('connector.connectors.requests.get')
    def test_get_movie_by_title_found(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'Response': 'True',
            'Title': 'Test Movie',
        }
        mock_requests_get.return_value = mock_response

        connector = OMDBConnector()
        result = connector.get_movie_by_title('Test Movie')

        self.assertEqual(result, [{'Response': 'True', 'Title': 'Test Movie'}])

    @patch('connector.connectors.requests.get')
    def test_get_movie_by_title_not_found(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'Response': 'False',
            'Error': 'Movie not found!',
        }
        mock_requests_get.return_value = mock_response

        connector = OMDBConnector()

        with self.assertRaises(NotFound):
            connector.get_movie_by_title('Nonexistent Movie')

    @patch('connector.connectors.requests.get')
    def test_get_movie_by_title_api_exception(self, mock_requests_get):
        mock_requests_get.side_effect = APIException('API Error')

        connector = OMDBConnector()

        with self.assertRaises(APIException):
            connector.get_movie_by_title('Test Movie')

    # Add more test cases for get_multiple_movies_by_title as needed
