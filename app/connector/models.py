from django.db import models


class MoviesModel(models.Model):
    id = models.AutoField(
        primary_key=True,
        help_text='A unique identifier for each movie',
    )
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    rated = models.CharField(max_length=10, blank=True)
    released = models.DateField(null=True, blank=True)
    runtime = models.CharField(max_length=10, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    director = models.CharField(max_length=255, blank=True)
    writer = models.CharField(max_length=255, blank=True)
    actors = models.CharField(max_length=255, blank=True)
    plot = models.TextField(blank=True)
    language = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    awards = models.CharField(max_length=255, blank=True)
    poster = models.URLField(blank=True)
    metascore = models.IntegerField(null=True, blank=True)
    imdb_rating = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    imdb_votes = models.IntegerField(null=True, blank=True)
    imdb_id = models.CharField(max_length=20, blank=True)
    dvd = models.DateField(null=True, blank=True)
    box_office = models.CharField(max_length=20, blank=True)
    production = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    response = models.BooleanField(default=False)
