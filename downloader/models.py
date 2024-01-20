from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    number_of_views = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")

    def __str__(self):
        return self.title
