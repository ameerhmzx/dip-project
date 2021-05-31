import math

import PIL.Image as PILImage
import cv2
import mtcnn
import numpy as np
from deepface.basemodels.Facenet import InceptionResNetV2

from .load_weights import get_weights


def euclidean_distance(src, test):
    distance = src - test
    distance = np.sum(np.multiply(distance, distance))
    distance = np.sqrt(distance)
    return distance


def align(img, left_eye, right_eye):
    left_eye_x, left_eye_y = left_eye
    right_eye_x, right_eye_y = right_eye
    if left_eye_y > right_eye_y:
        point_3rd = (right_eye_x, left_eye_y)
        direction = -1
    else:
        point_3rd = (left_eye_x, right_eye_y)
        direction = 1
    a = euclidean_distance(np.array(left_eye), np.array(point_3rd))
    b = euclidean_distance(np.array(right_eye), np.array(point_3rd))
    c = euclidean_distance(np.array(right_eye), np.array(left_eye))
    if b != 0 and c != 0:
        cos_a = (b * b + c * c - a * a) / (2 * b * c)
        angle = np.arccos(cos_a)
        angle = (angle * 180) / math.pi
        if direction == -1:
            angle = 90 - angle
        img = PILImage.fromarray(img)
        img = np.array(img.rotate(direction * angle))
    return img


def get_faces(image):
    if image.shape[0] < 0 or image.shape[1] < 0:
        return []

    face_detector = mtcnn.MTCNN()
    detections = face_detector.detect_faces(image)

    faces = []
    aligned_faces = []
    facenet_model = None

    if len(detections) > 0:
        facenet_model = InceptionResNetV2()
        facenet_model.load_weights(get_weights("facenet"))

    for face in detections:
        y, x, h, w = face['box']
        extracted_img = image[x:x + w, y:y + h]

        left_eye = face['keypoints']['left_eye']
        right_eye = face['keypoints']['right_eye']
        a_img = align(extracted_img, left_eye, right_eye)
        a_img = cv2.resize(a_img, (160, 160))
        aligned_faces.append(a_img)

        aligned_faces = aligned_faces / 255
        img_pixels = np.expand_dims(aligned_faces, axis=0)
        embeddings = facenet_model.predict(img_pixels)

        faces.append({
            'bbox': face['box'],
            'confidence': face['confidence'],
            'embeddings': embeddings,
        })

    return faces
