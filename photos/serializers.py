import json

from rest_framework import serializers

from . import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ['id', 'name']


class FaceSerializer(serializers.ModelSerializer):
    bbox = serializers.SerializerMethodField()
    person = PersonSerializer()

    def get_bbox(self, obj):
        return [obj.top, obj.left, obj.height, obj.width]

    class Meta:
        model = models.Face
        fields = ['id', 'bbox', 'confidence', 'person']


class PhotoSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()
    faces = FaceSerializer(many=True)

    def get_meta(self, obj):
        return json.loads(obj.meta or 'null')

    class Meta:
        model = models.Photo
        fields = ['id', 'name', 'description', 'image', 'thumbnail', 'meta', 'faces']
        read_only_fields = ['image', 'thumbnail', 'meta', 'faces']
