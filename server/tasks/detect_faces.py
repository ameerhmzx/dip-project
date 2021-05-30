import math

import mtcnn
import numpy as np
import cv2
import PIL.Image as PILImage


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

        # should be some other way to rotate images in numpy
        # without converting to PIL Image just for rotation
        img = PILImage.fromarray(img)
        img = np.array(img.rotate(direction * angle))
    return img


def get_faces(image):
    annotated = image.copy()

    if image.shape[0] < 0 or image.shape[1] < 0: return ([], [], annotated)

    face_detector = mtcnn.MTCNN()
    detections = face_detector.detect_faces(image)

    faces = []
    aligned_faces = []

    for face in detections:
        y, x, h, w = face['box']
        extracted_img = image[x:x + w, y:y + h]
        faces.append(extracted_img)

        cv2.rectangle(annotated, (y, x), (y + h, x + w), (255, 0, 0), 2)

        left_eye = face['keypoints']['left_eye']
        right_eye = face['keypoints']['right_eye']
        a_img = align(extracted_img, left_eye, right_eye)
        a_img = cv2.resize(a_img, (160, 160))
        aligned_faces.append(a_img)

    return faces, aligned_faces, annotated
