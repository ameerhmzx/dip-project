import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField


class Face(models.Model):
    name = models.CharField(max_length=255)
    # featured_photo = models.ImageField()

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=lambda: f'photos/{str(uuid.uuid4())}')
    thumbnail = models.ImageField(upload_to=lambda: f'photos/{str(uuid.uuid4())}')

    faces = models.ManyToManyField(Face)
    meta = JSONField(blank=True, null=True)
