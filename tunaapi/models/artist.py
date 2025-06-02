from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    bio = models.TextField()
