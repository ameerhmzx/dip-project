from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View

from PIL import Image

from .tasks import extract_meta, extract_faces


class ImageView(View):
    def post(self, request):
        photo = request.FILES['photo']
        if not photo:
            return HttpResponseBadRequest()

        image = Image.open(photo)

        meta = extract_meta(image)
        faces = extract_faces(image)
        print(meta, flush=True)
        print(faces, flush=True)

        return HttpResponse('result')
