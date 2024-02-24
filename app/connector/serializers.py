from rest_framework import serializers

from connector.models import MoviesModel


class MoviesSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        # Define key mappings
        key_mappings = {
            'Title': 'title',
            'Year': 'year',
            'Rated': 'rated',
            'Released': 'released',
            'Runtime': 'runtime',
            'Genre': 'genre',
            'Director': 'director',
            'Writer': 'writer',
            'Actors': 'actors',
            'Plot': 'plot',
            'Language': 'language',
            'Country': 'country',
            'Awards': 'awards',
            'Poster': 'poster',
            'Metascore': 'metascore',
            'imdbRating': 'imdb_rating',
            'imdbVotes': 'imdb_votes',
            'imdbID': 'imdb_id',
            'DVD': 'dvd',
            'BoxOffice': 'box_office',
            'Production': 'production',
            'Website': 'website',
            'Response': 'response',
        }

        # Map keys to corresponding fields
        converted_data = {
            key_mappings.get(key, key): value for key, value in data.items()
        }

        return super().to_internal_value(converted_data)

    class Meta:
        model = MoviesModel
        fields = '__all__'


class MovieRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)


class MovieParameterSizeSerializer(serializers.Serializer):
    limit = serializers.IntegerField(max_value=100, default=10, required=False)
    title = serializers.CharField(
        max_length=50, required=False, allow_null=True
    )
