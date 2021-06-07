import io
import json

from PIL import Image, ImageCms
from PIL.ExifTags import TAGS

from photos.celery import app
from photos.models import Photo


def no_op(x): return x


ALLOWED_TAGS = {
    'XResolution': float,
    'YResolution': float,
    'Make': no_op,
    'Model': no_op,
    'Software': no_op,
    'DateTime': no_op,
    'ApertureValue': float,
    'ExposureTime': float,
    'ShutterSpeedValue': float,
    'FocalLength': float,
    'ISOSpeedRatings': no_op,
    'MeteringMode': no_op,
    'Flash': no_op,
    'FNumber': float,
    'ExposureProgram': no_op,
    'WhiteBalance': no_op,
    'LensMake': no_op,
    'LensModel': no_op,
    'GPSInfo': lambda val: (
        dms_to_decimal(val[2], val[1]),
        dms_to_decimal(val[4], val[3]),
    )
}


def get_color_info(image: Image):
    icc_profile = image.info.get('icc_profile', None)
    if not icc_profile:
        return {}

    profile = ImageCms.ImageCmsProfile(io.BytesIO(icc_profile))
    return {
        'ColorProfile': profile.profile.profile_description,
        'ColorSpace': profile.profile.xcolor_space
    }


def dms_to_decimal(dms, ref):
    d, m, s = dms
    if ref in ['S', 'W']:
        d, m, s = -d, -m, -s
    return round(d + m / 60.0 + s / 3600.0, 6)


def get_exif_data(image: Image):
    raw_exif = getattr(image, '_getexif', lambda: None)()
    return {
        TAGS[k]: ALLOWED_TAGS[TAGS[k]](v)
        for (k, v) in raw_exif.items()
        if ALLOWED_TAGS.get(TAGS.get(k, ''), False)
    }


@app.task
def extract_meta(image_path: str, pk: int):
    image = Image.open(image_path)

    color_info = get_color_info(image)
    exif_data = get_exif_data(image)

    meta = {**color_info, **exif_data}
    photo = Photo.objects.get(pk=pk)
    photo.meta = json.dumps(meta)
    photo.save()
