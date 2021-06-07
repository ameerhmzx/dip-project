from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from elasticsearch.exceptions import NotFoundError

from photos.elastic_search import set_person, delete_embeddings
from photos.state_aware_model import StateAwareModel


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
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)

    def delete(self, *args, **kwargs):
        self.image.storage.delete(self.image.name)
        self.thumbnail.storage.delete(self.thumbnail.name)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Face(StateAwareModel):
    left = models.PositiveIntegerField()
    top = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    confidence = models.FloatField()
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='faces')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            dirty_fields = self.get_dirty_fields()

            if 'person_id' in dirty_fields:
                set_person(self.pk, -1 if self.person_id is None else self.person_id)

        super().save(*args, **kwargs)


class DetectedObject(models.Model):
    left = models.PositiveIntegerField()
    top = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    confidence = models.FloatField()
    name = models.CharField(max_length=255)
    info = JSONField()
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='detected_objects')

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Face)
def delete_face(sender, instance, **kwargs):
    return
    # try:
    #     delete_embeddings(instance.pk)
    # except NotFoundError:
    #     pass
