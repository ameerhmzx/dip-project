from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.http import HttpResponseBadRequest
from rest_framework import generics
from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoSerializer


from .tasks import extract_meta, extract_faces, extract_objects


def image_to_file(image: Image, name):
    img_io = BytesIO()
    image.save(img_io, format='PNG', quality=100)
    return ContentFile(img_io.getvalue(), name)


class PhotoListView(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def post(self, request):
        photo = request.FILES['photo']
        if not photo:
            return HttpResponseBadRequest()

        image = Image.open(photo)
        thumbnail = image.copy().thumbnail((200, 200))

        photo_obj = Photo.objects.create(
            name=photo.name,
            image=image_to_file(image, photo.name),
            thumbnail=image_to_file(thumbnail, "thb_" + photo.name)
        )

        extract_meta.delay(photo_obj.image.path, photo_obj.id)
        extract_faces.delay(photo_obj.image.path, photo_obj.id)
        extract_objects.delay(photo_obj.image.path, photo_obj.id)

        serializer = PhotoSerializer(photo_obj)
        return Response(serializer.data)


class PhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
