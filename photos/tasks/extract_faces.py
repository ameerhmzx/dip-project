import math
from typing import TypedDict, Tuple, Any

import cv2
import numpy as np
from PIL import Image

from photos import models
from photos.celery import app
from photos.elastic_search import save_embeddings, recognize_person
from .load_weights import get_weights


class Face(TypedDict):
    """Just for type declaration"""
    bbox: Tuple[int, int, int, int]
    confidence: float
    embeddings: Any


def align(img, left_eye, right_eye):
    """align face image by aligned left and right eye in straight line"""
    left_eye_x, left_eye_y = left_eye
    right_eye_x, right_eye_y = right_eye
    point_3rd, direction = (left_eye, -1) if left_eye_y > right_eye_y else (right_eye, 1)

    # np.linalg.norm is being used for euclidean distance
    a = np.linalg.norm(np.array(left_eye) - np.array(point_3rd))
    b = np.linalg.norm(np.array(right_eye) - np.array(point_3rd))
    c = np.linalg.norm(np.array(right_eye) - np.array(left_eye))

    if b != 0 and c != 0:
        angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
        angle = (angle * 180) / math.pi
        if direction == -1:
            angle = 90 - angle
        img = Image.fromarray(img)
        img = np.array(img.rotate(direction * angle))

    return img


def normalize_face(image: Image, face):
    """normalize face image before passing it to model"""
    y, x, h, w = face['box']
    cropped_face = image[x:x + w, y:y + h]

    left_eye = face['keypoints']['left_eye']
    right_eye = face['keypoints']['right_eye']
    aligned_face = align(cropped_face, left_eye, right_eye)
    aligned_face = cv2.resize(aligned_face, (160, 160))

    return np.expand_dims(aligned_face / 255, axis=0)


@app.task
def extract_faces(image_path: str, pk: int):
    """extract faces from the given image"""
    image = Image.open(image_path)
    image = np.array(image)

    if image.shape[0] <= 0 or image.shape[1] <= 0:
        return None

    import mtcnn

    # detect faces from image
    face_detector = mtcnn.MTCNN()
    detections = face_detector.detect_faces(image)

    if len(detections) < 1:
        return None

    from deepface.basemodels.Facenet import InceptionResNetV2

    # load InceptionResNet model provided by deepface
    facenet_model = InceptionResNetV2()
    facenet_model.load_weights(get_weights("facenet"))

    # normalize faces and get embeddings
    faces = [normalize_face(image, face) for face in detections]
    embeddings = facenet_model.predict(np.vstack(faces), batch_size=len(faces))

    for i in range(len(faces)):
        person_id = recognize_person(embeddings[i])
        print(person_id, flush=True)
        face_obj = models.Face.objects.create(
            confidence=detections[i]['confidence'],
            left=detections[i]['box'][0],
            top=detections[i]['box'][1],
            width=detections[i]['box'][2],
            height=detections[i]['box'][3],
            photo_id=pk,
            person_id=person_id
        )

        save_embeddings(embeddings[i], face_obj.id, person_id)
