from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.http import HttpResponseBadRequest
from rest_framework import generics
from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoSerializer


# from .tasks import extract_meta


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


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
        thumbnail = crop_center(image, 156, 106)

        photo_obj = Photo.objects.create(
            name=photo.name,
            image=image_to_file(image, photo.name),
            thumbnail=image_to_file(thumbnail, "thb_" + photo.name)
        )

        serializer = PhotoSerializer(photo_obj)
        return Response(serializer.data)


class PhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
