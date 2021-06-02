from django.db import models
from django.contrib.postgres.fields import JSONField


class Person(models.Model):
    name = models.CharField(max_length=255)
    # featured_photo = models.ImageField()

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='photos/')
    meta = JSONField(blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        self.thumbnail.storage.delete(self.thumbnail.name)
        super().delete()

    def __str__(self):
        return self.name


class Face(models.Model):
    left = models.PositiveIntegerField()
    top = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    confidence = models.FloatField()
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='faces')
