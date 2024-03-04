from django.test import TestCase
from django.urls import resolve


class TestUrls(TestCase):
    def test_movies_url(self):
        resolver = resolve('/api/movies')
        self.assertEqual(resolver.view_name, 'movies')
