"""View module for handling requests about song genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre, Song, Genre


class SongGenreView(ViewSet):
    """Tuna API song genre view"""

    def create(self, request):
        """Handle POST requests for song genres

        Returns: JSON serialized song genres
        """
        song = Song.objects.get(pk=request.data["song"])
        genre = Genre.objects.get(pk=request.data["genre"])
        songGenre = SongGenre.objects.create(
            song=song,
            genre=genre
        )
        serializer = SongGenreSerializer(songGenre)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all song genres

        Returns: JSON serialized list of all song genres
        """
        song_genres = SongGenre.objects.all()

        serializer = AllSongGenreSerializer(song_genres, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handle DELETE requests for song genres

        Returns: empty body with 204 status code"""

        song_genre = SongGenre.objects.get(pk=pk)
        song_genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres"""

    class Meta:
        model = SongGenre
        fields = ('id', 'song', 'genre')


class AllSongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres"""

    class Meta:
        model = SongGenre
        fields = ('id', 'song', 'genre')
        depth = 2
