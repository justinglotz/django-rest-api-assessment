"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, Song
from rest_framework.decorators import action
from django.db.models import Count


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

    @action(methods=['get'], detail=False)
    def popular(self, request):
        """GET request to get popular genres"""
        # Gets list of genre objects that have an entry in SongGenre(this counts the songs without needing a join table)
        # Orders by song count, DESCENDING (not django's default)
        genres = Genre.objects.annotate(
            song_count=Count('songgenre')).order_by('-song_count')
        serializer = PopularGenreSerializer(genres, many=True)
        return Response({'genres': serializer.data})


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


class PopularGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for list of genres by song count"""
    song_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Genre
        fields = ('id', 'description', 'song_count')
