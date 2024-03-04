from datetime import datetime

from django.test import TestCase

from connector.serializers import (
    MovieParameterSizeSerializer,
    MovieRequestSerializer,
    MoviesSerializer,
)


class MoviesSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'Title': 'Test Movie',
            'Year': '2022',
            'Rated': 'PG-13',
            'Released': '10 Apr 2022',
            'Runtime': '120 min',
            'Genre': 'Action, Adventure',
            'Director': 'Test Director',
            'Writer': 'Test Writer',
            'Actors': 'Actor1, Actor2',
            'Plot': 'Test plot.',
            'Language': 'English',
            'Country': 'USA',
            'Awards': 'Best Picture',
            'Poster': 'http://example.com/poster.jpg',
            'Metascore': '75',
            'imdbRating': '8.0',
            'imdbVotes': '1000',
            'imdbID': 'tt1234567',
            'DVD': '10 May 2022',
            'BoxOffice': '$10,000,000',
            'Production': 'Test Production',
            'Website': 'http://example.com',
            'Response': 'True',
        }
        self.invalid_data = {
            'Title': 'A' * 256,  # Exceeds max length
        }

    def test_valid_data(self):
        serializer = MoviesSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        converted_data = serializer.to_internal_value(self.valid_data)
        self.assertEqual(converted_data['title'], 'Test Movie')
        self.assertEqual(converted_data['year'], '2022')
        self.assertEqual(converted_data['rated'], 'PG-13')
        self.assertEqual(
            converted_data['released'], datetime(2022, 4, 10).date()
        )
        self.assertEqual(converted_data['runtime'], '120 min')
        self.assertEqual(converted_data['genre'], 'Action, Adventure')
        # Add more assertions for other fields

    def test_invalid_data(self):
        serializer = MoviesSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Title', serializer.errors)

    # Add more test cases as needed


class MovieRequestSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {'title': 'Test Title'}
        self.invalid_data = {'title': 'A' * 51}

    def test_valid_data(self):
        serializer = MovieRequestSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], 'Test Title')

    def test_invalid_title_length(self):
        serializer = MovieRequestSerializer(data={'title': 'A' * 51})
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_missing_title(self):
        serializer = MovieRequestSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


class MovieParameterSizeSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {'limit': 50, 'title': 'Test Title'}
        self.invalid_data = {'limit': 200, 'title': 'A' * 51}

    def test_valid_data(self):
        serializer = MovieParameterSizeSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['limit'], 50)
        self.assertEqual(serializer.validated_data['title'], 'Test Title')

    def test_default_limit(self):
        serializer = MovieParameterSizeSerializer(data={'title': 'Test Title'})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['limit'], 10)

    def test_invalid_limit(self):
        serializer = MovieParameterSizeSerializer(data={'limit': 200})
        self.assertFalse(serializer.is_valid())
        self.assertIn('limit', serializer.errors)

    def test_invalid_title_length(self):
        serializer = MovieParameterSizeSerializer(data={'title': 'A' * 51})
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
