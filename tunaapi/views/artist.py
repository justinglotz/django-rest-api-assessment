"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song, SongGenre, Genre
from rest_framework.decorators import action

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

    @action(methods=['get'], detail=True)
    def related(self, request, pk):
        """GET request to get related artists"""
        # Get the artist for this request
        this_artist = Artist.objects.get(pk=pk)

        # Filter songGenre instances where the artist attribute of the song is the same as this one
        filtered_songgenres = SongGenre.objects.filter(
            song__artist=this_artist)
        most_common = (
            # The values of all the genre fields in filtered_songgenres
            filtered_songgenres.values('genre')
            # For each genre, count the number of times that genre appears in the queryset
            .annotate(count=Count('genre'))
            # Order by count, with the most represented genre listed first
            .order_by('-count')
            # Get the first entry, which should be the most common genre in the list
            .first()
        )
        this_artist.most_common_genre = most_common['genre'] if most_common else None

        related_artists = []
        artists = Artist.objects.exclude(pk=pk)
        for artist in artists:
            filtered_songgenres = SongGenre.objects.filter(
                song__artist=artist)
            most_common = (
                # The values of all the genre fields in filtered_songgenres
                filtered_songgenres.values('genre')
                # For each genre, count the number of times that genre appears in the queryset
                .annotate(count=Count('genre'))
                # Order by count, with the most represented genre listed first
                .order_by('-count')
                # Get the first entry, which should be the most common genre in the list
                .first()
            )
            artist.most_common_genre = most_common['genre'] if most_common else None
            if artist.most_common_genre is not None and artist.most_common_genre == this_artist.most_common_genre:
                related_artists.append(artist)
        serializer = RelatedArtistSerializer(related_artists, many=True)
        return Response({'artists': serializer.data})


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


class RelatedArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for related artists"""

    class Meta:
        model = Artist
        fields = ('id', 'name')
