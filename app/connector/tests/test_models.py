from django.test import TestCase

from connector.models import MoviesModel


class MoviesModelTest(TestCase):
    def setUp(self):
        self.movie_data = {
            'title': 'Test Movie',
            'year': '2022',
            'rated': 'PG-13',
            'released': '2022-01-01',
            'runtime': '120 min',
            'genre': 'Action, Adventure',
            'director': 'Test Director',
            'writer': 'Test Writer',
            'actors': 'Actor1, Actor2',
            'plot': 'Test plot.',
            'language': 'English',
            'country': 'USA',
            'awards': 'Best Picture',
            'poster': 'http://example.com/poster.jpg',
            'metascore': 75,
            'imdb_rating': 8.0,
            'imdb_votes': 1000,
            'imdb_id': 'tt1234567',
            'dvd': '2022-05-10',
            'box_office': '$10,000,000',
            'production': 'Test Production',
            'website': 'http://example.com',
            'response': True,
        }

    def tearDown(self):
        # Clean up created objects
        MoviesModel.objects.all().delete()

    def test_create_movie(self):
        movie = MoviesModel.objects.create(**self.movie_data)
        self.assertEqual(movie.title, 'Test Movie')
        self.assertEqual(movie.year, '2022')
        self.assertEqual(movie.rated, 'PG-13')

    def test_create_movie_missing_optional_fields(self):
        minimal_movie_data = {
            'title': 'Minimal Movie',
        }
        movie = MoviesModel.objects.create(**minimal_movie_data)
        self.assertEqual(movie.title, 'Minimal Movie')
        self.assertIsNone(movie.year)
        self.assertIsNone(movie.rated)
