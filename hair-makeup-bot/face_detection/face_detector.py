import dlib
import numpy as np


class FaceDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()

    def get_faces_bbox(self, img: np.ndarray) -> dlib.rectangles:
        """ Extract face_detection bounding boxes

        :param img: the input image
        :return: the face_detection bounding boxes
        :raise IndexError if no face has been found
        """
        rects: dlib.rectangles = self.detector(img)
        if len(rects) == 0:
            raise IndexError('No face_detection found')
        return rects

    def get_single_face_bbox(self, img: np.ndarray) -> dlib.rectangle:
        """ Extract first face bounding box

        :param img: the input image
        :return: the first face bounding box
        :raise IndexError if no face has been found
        """
        rect = self.get_faces_bbox(img)[0]
        return rect
