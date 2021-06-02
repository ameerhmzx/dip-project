import contextlib
import json
import os

from photos.celery import app
from photos.models import DetectedObject


@contextlib.contextmanager
def cd(path):
    CWD = os.getcwd()
    os.chdir(path)
    try:
        yield
    except Exception as e:
        print(e)
    finally:
        os.chdir(CWD)


yolo_detector = None


def load_detector():
    global yolo_detector

    from yolov4 import Detector
    if yolo_detector is not None:
        return yolo_detector

    with cd('/usr/local/bin/darknet'):
        yolo_detector = Detector(gpu_id=0, weights_path='/photos/weights/yolov4.weights')

    return yolo_detector


@app.task
def extract_objects(image_path: str, pk: int):
    detector = load_detector()
    detections = detector.perform_detect(image_path_or_buf=image_path, show_image=False)

    for detection in detections:
        if detection.class_confidence < 0.7 or detection.class_name == 'person':
            continue
        DetectedObject.objects.create(
            name=detection.class_name,
            confidence=detection.class_confidence,
            left=detection.left_x,
            top=detection.top_y,
            width=detection.width,
            height=detection.height,
            info=json.dumps(detection.info),
            photo_id=pk
        )
