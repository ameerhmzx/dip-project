from django.contrib import admin
from . import models


class FaceInline(admin.TabularInline):
    model = models.Face


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    inlines = (FaceInline, )


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    pass
