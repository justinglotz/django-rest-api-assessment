"""View module for handling requests about songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, Genre, SongGenre
from tunaapi.views import GenreSerializer


class SongView(ViewSet):
    """Tuna API songs view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song

        Returns: JSON serialized song
        """
        song = Song.objects.get(pk=pk)
        serializer = SingleSongSerializer(song)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all songs

        Returns: JSON serialized list of all songs
        """
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests for songs

        Returns: JSON serialized song instance
        """
        artist = Artist.objects.get(pk=request.data["artist_id"])

        song = Song.objects.create(
            title=request.data["title"],
            artist=artist,
            album=request.data["album"],
            length=request.data["length"]
        )

        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a song

        Returns: empty body with 204 status code"""
        artist = Artist.objects.get(pk=request.data["artist_id"])

        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.artist = artist
        song.album = request.data["album"]
        song.length = request.data["length"]
        song.save()

        serializer = SongSerializer(song)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handle DELETE requests for song

        Returns: empty body with 204 status code"""

        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')


class SingleSongSerializer(serializers.ModelSerializer):
    """JSON serializer for a single song"""
    # This is saying the genres field needs its own logic, django will look for the get_genres function to determine the logic. It will look for get_fieldname for whatever the field name is
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'length', 'genres')
        depth = 1

    def get_genres(self, obj):
        # Get genre records. Look at the SongGenre table, find where the song field in the songgenre table (songgenre__song) equals our current song (obj)
        genres = Genre.objects.filter(songgenre__song=obj)
        return GenreSerializer(genres, many=True).data
