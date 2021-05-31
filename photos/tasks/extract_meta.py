import io
from datetime import datetime

from PIL import Image, ImageCms
from PIL.ExifTags import TAGS

from photos.celery import app


def no_op(x): return x


ALLOWED_TAGS = {
    'XResolution': no_op,
    'YResolution': no_op,
    'Make': no_op,
    'Model': no_op,
    'Software': no_op,
    'DateTime': lambda x: datetime.strptime(x, '%Y:%m:%d %H:%M:%S'),
    'ApertureValue': no_op,
    'ExposureTime': no_op,
    'ShutterSpeedValue': no_op,
    'FocalLength': no_op,
    'ISOSpeedRatings': no_op,
    'MeteringMode': no_op,
    'Flash': no_op,
    'FNumber': no_op,
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
    icc_profile = image.info.get('icc_profile')
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
def extract_meta(image: Image):
    color_info = get_color_info(image)
    exif_data = get_exif_data(image)

    return {**color_info, **exif_data}
