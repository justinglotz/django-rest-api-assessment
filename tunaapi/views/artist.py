"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song
from django.db.models import Count


class ArtistView(ViewSet):
    """Tuna API artists view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist

        Returns: JSON serialized artist
        """
        # artist = Artist.objects.get(pk=pk)
        artist = Artist.objects.filter(pk=pk).annotate(
            song_count=Count('songs')).first()
        serializer = SingleArtistSerializer(artist)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all artists

        Returns: JSON serialized list of all artists
        """
        artists = Artist.objects.all()

        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests for artists

        Returns: JSON serialized artist instance
        """
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"]
        )

        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an artist

        Returns: empty body with 204 status code"""

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()

        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handle DELETE requests for artist

        Returns: empty body with 204 status code"""

        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists"""

    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')


class SingleArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for single artist"""
    song_count = serializers.IntegerField(default=None)

    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth = 1
