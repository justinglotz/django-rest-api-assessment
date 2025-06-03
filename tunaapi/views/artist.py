"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist


class ArtistView(ViewSet):
    """Tuna API artists view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist

        Returns: JSON serialized artist
          """
        artist = Artist.objects.get(pk=pk)
        serializer = ArtistSerializer(artist)

    def create(self, request):
        """Handle POST requests for artists

        Returns: JSON serialized artist instance"""
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"]
        )

        serializer = ArtistSerializer(artist)
        return Response(serializer.data)


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists"""

    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')
