from django.urls import path

from . import views

urlpatterns = [
    path(
        'movies',
        views.MoviesView.as_view({'post': 'create', 'get': 'list'}),
        name='movies',
    ),
    path(
        'movies/<str:movie_id>',
        views.MoviesView.as_view(
            {'get': 'retrieve', 'delete': 'delete', 'put': 'partial_update'}
        ),
        name='movies',
    ),
]
