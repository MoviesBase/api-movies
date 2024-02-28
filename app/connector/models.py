from django.db import models


class MoviesModel(models.Model):
    id = models.AutoField(
        primary_key=True, help_text='A unique identifier for each movie'
    )
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4, null=True, blank=True)
    rated = models.CharField(max_length=10, blank=True, null=True)
    released = models.DateField(null=True, blank=True)
    runtime = models.CharField(max_length=10, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    writer = models.CharField(max_length=255, blank=True, null=True)
    actors = models.CharField(max_length=255, blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    awards = models.CharField(max_length=255, blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    metascore = models.IntegerField(null=True, blank=True)
    imdb_rating = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    imdb_votes = models.FloatField(null=True, blank=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    dvd = models.DateField(null=True, blank=True)
    box_office = models.CharField(max_length=20, blank=True, null=True)
    production = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    response = models.BooleanField(default=False)
