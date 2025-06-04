"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, Song


class GenreView(ViewSet):
    """Tuna API genres view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single genre

        Returns: JSON serialized genre
        """
        genre = Genre.objects.get(pk=pk)
        serializer = SingleGenreSerializer(genre)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all genres

        Returns: JSON serialized list of all genres
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests for genres

        Returns: JSON serialized genre instance
        """
        genre = Genre.objects.create(
            description=request.data["description"]
        )

        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a genre

        Returns: empty body with 204 status code"""

        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()

        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handle DELETE requests for genre

        Returns: empty body with 204 status code"""

        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres"""

    class Meta:
        model = Genre
        fields = ('id', 'description')


class SingleGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for a single genre"""
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')

    def get_songs(self, obj):
        from tunaapi.views import SongSerializer
        songs = Song.objects.filter(songgenre__genre=obj)
        return SongSerializer(songs, many=True).data
