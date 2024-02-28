from datetime import datetime

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
        for key, value in converted_data.items():
            if value == 'N/A':
                converted_data[key] = None
            else:
                continue
        if converted_data.get('imdb_votes'):
            converted_data['imdb_votes'] = float(
                str(converted_data['imdb_votes']).replace(',', '.')
            )

        date_fields = ['dvd', 'released']
        # Loop through each date field
        for field in date_fields:
            # Parse the date string into a datetime object
            try:
                if converted_data.get(field):
                    parsed_date = datetime.strptime(
                        converted_data[field], '%d %b %Y'
                    )
                    converted_data[field] = parsed_date.date()
            except ValueError:
                raise serializers.ValidationError(
                    f"Invalid date format for {field}. Please use 'DD Mon YYYY' format."
                )
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
