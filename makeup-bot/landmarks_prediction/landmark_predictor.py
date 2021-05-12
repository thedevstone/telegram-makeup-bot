import dlib
import numpy as np

from file_manager.path_utilities import get_model_path
from landmarks_prediction.conversions import landmarks_to_array


class LandmarkPredictor:
    def __init__(self, predictor_type='dlib'):
        """ Initialize the landmark predictor

        :param predictor_type: the predictor type. 'dlib' for standard fast predictor or 'dnn' for slow deep predictor
        """
        self.predictor_type = predictor_type
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(get_model_path('shape_predictor_68_face_landmarks.dat'))

    def get_2d_landmarks(self, img: np.ndarray) -> np.ndarray:
        """
        Get 2d dlib's landmarks_prediction

        :param img: the image
        :return: a list of landmark parts
        """
        faces_bbox = self.detector(img)
        if len(faces_bbox) == 0:
            raise IndexError("No faces has been found")
        return self.get_2d_landmarks_from_bbox(img, faces_bbox[0])

    def get_2d_landmarks_from_bbox(self, img: np.ndarray, bbox: dlib.rectangle) -> np.ndarray:
        """
        Get 2d dlib's landmarks_prediction

        :param img: the image
        :param bbox: the region of extraction
        :return: a list of landmark parts
        """
        landmarks = self.predictor(img, bbox)
        landmarks_2d = landmarks_to_array(landmarks)
        return landmarks_2d
