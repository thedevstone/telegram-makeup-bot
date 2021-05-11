import cv2
import dlib
import numpy as np

from image_alterations_detector.face_morphology.face_detection.conversions import rect_to_bounding_box


def draw_faces_bounding_boxes(img: np.ndarray, rects: dlib.rectangles):
    """ Draw the face bounding boxes

    :param img: the input image
    :param rects: the dlib rectangles
    :return: a new image with bboxes
    """
    img_out = np.array(img)
    # loop over the face detections
    for (i, rect) in enumerate(rects):
        (x, y, w, h) = rect_to_bounding_box(rect)
        cv2.rectangle(img_out, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return img_out
