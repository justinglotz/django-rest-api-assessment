from django.db import models
from .artist import Artist


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.CharField(max_length=200)
    length = models.PositiveIntegerField()
