from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View

from PIL import Image

from .tasks import extract_meta


class ImageView(View):
    def post(self, request):
        photo = request.FILES['photo']
        if not photo:
            return HttpResponseBadRequest()

        image = Image.open(photo)

        data = extract_meta(image)
        print(data, flush=True)

        return HttpResponse('result')
