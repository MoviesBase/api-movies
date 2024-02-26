# Generated by Django 3.2.24 on 2024-02-26 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoviesModel',
            fields=[
                ('id', models.AutoField(help_text='A unique identifier for each movie', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=4)),
                ('rated', models.CharField(blank=True, max_length=10)),
                ('released', models.DateField(blank=True, null=True)),
                ('runtime', models.CharField(blank=True, max_length=10)),
                ('genre', models.CharField(blank=True, max_length=255)),
                ('director', models.CharField(blank=True, max_length=255)),
                ('writer', models.CharField(blank=True, max_length=255)),
                ('actors', models.CharField(blank=True, max_length=255)),
                ('plot', models.TextField(blank=True)),
                ('language', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(blank=True, max_length=255)),
                ('awards', models.CharField(blank=True, max_length=255)),
                ('poster', models.URLField(blank=True)),
                ('metascore', models.IntegerField(blank=True, null=True)),
                ('imdb_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('imdb_votes', models.IntegerField(blank=True, null=True)),
                ('imdb_id', models.CharField(blank=True, max_length=20)),
                ('dvd', models.DateField(blank=True, null=True)),
                ('box_office', models.CharField(blank=True, max_length=20)),
                ('production', models.CharField(blank=True, max_length=255)),
                ('website', models.URLField(blank=True)),
                ('response', models.BooleanField(default=False)),
            ],
        ),
    ]