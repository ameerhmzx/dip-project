import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField


def uuid_photo(ins, name):
    return f'photos/{str(uuid.uuid4())}'


class Face(models.Model):
    name = models.CharField(max_length=255)
    # featured_photo = models.ImageField()

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='photos/')

    faces = models.ManyToManyField(Face)
    meta = JSONField(blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        self.thumbnail.storage.delete(self.thumbnail.name)
        super().delete()

    def __str__(self):
        return self.name
