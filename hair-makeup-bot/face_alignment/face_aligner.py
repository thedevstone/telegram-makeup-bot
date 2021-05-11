# import the necessary packages
from typing import Tuple

import cv2
import numpy as np

from landmarks_prediction.landmark_predictor import LandmarkPredictor
from landmarks_prediction.utils import FACIAL_LANDMARKS_68_INDEXES, FACIAL_LANDMARKS_5_INDEXES


class FaceAligner:
    def __init__(self, left_eye_percentage=(0.40, 0.40), desired_face_width=256, desired_face_height=None,
                 predictor_type='dlib'):
        """ Define aligner for all images.

        :param left_eye_percentage: An optional (x, y) tuple with the default shown, specifying the desired output left eye position. For this variable, it is common to see percentages within the range of 20-40%. These percentages control how much of the face is visible after alignment. The exact percentages used will vary on an application-to-application basis. With 20% you’ll basically be getting a “zoomed in” view of the face, whereas with larger values the face will appear more “zoomed out.”.
        :param desired_face_width: optional parameter that defines our desired face with in pixels.
        :param desired_face_height: optional parameter specifying our desired face height value in pixels
        :param predictor_type: the predictor type. 'dlib' for standard fast predictor or 'dnn' for slow deep predictor
        """
        self.left_eye_percentage = left_eye_percentage
        self.desired_face_width = desired_face_width
        self.desired_face_height = desired_face_height
        self.predictor = LandmarkPredictor(predictor_type)
        if self.desired_face_height is None:
            self.desired_face_height = self.desired_face_width

    def align(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """ Align image according to eye position

        :param image: the image
        :return: the aligned image

        .. warning:: High computational cost for landmark computation
        """
        # Extract the left and right eye (x, y)-coordinates
        shape = self.predictor.get_2d_landmarks(image)
        if len(shape) == 68:
            (lStart, lEnd) = FACIAL_LANDMARKS_68_INDEXES["left_eye"]
            (rStart, rEnd) = FACIAL_LANDMARKS_68_INDEXES["right_eye"]
        else:
            (lStart, lEnd) = FACIAL_LANDMARKS_5_INDEXES["left_eye"]
            (rStart, rEnd) = FACIAL_LANDMARKS_5_INDEXES["right_eye"]
        # Get eye points
        left_eye_pts = shape[lStart:lEnd]
        right_eye_pts = shape[rStart:rEnd]
        # Compute the center of mass for each eye
        left_eye_center = left_eye_pts.mean(axis=0).astype("int")
        right_eye_center = right_eye_pts.mean(axis=0).astype("int")
        # Compute the angle between the eye centroids
        d_y = right_eye_center[1] - left_eye_center[1]
        d_x = right_eye_center[0] - left_eye_center[0]
        angle = np.degrees(np.arctan2(d_y, d_x)) - 180
        # Compute the desired right eye x-coordinate based on the desired x-coordinate of the left eye
        right_eye_percentage_x = 1.0 - self.left_eye_percentage[0]
        # Determine the scale of the new resulting image by taking the ratio of the distance between eyes in the current
        # Image to the ratio of distance between eyes in the desired image
        dist = np.sqrt((d_x ** 2) + (d_y ** 2))
        dist_percentage = (right_eye_percentage_x - self.left_eye_percentage[0])
        desired_dist = self.desired_face_width * dist_percentage
        scale = desired_dist / dist

        # Compute center (x, y)-coordinates (i.e., the median point) between the two eyes in the input image
        eyes_center = ((left_eye_center[0] + right_eye_center[0]) // 2,
                       (left_eye_center[1] + right_eye_center[1]) // 2)

        # Grab the rotation matrix for rotating and scaling the face
        rotation_matrix = cv2.getRotationMatrix2D(eyes_center, angle, scale)

        # Update the translation component of the matrix
        t_x = self.desired_face_width * 0.5
        t_y = self.desired_face_height * self.left_eye_percentage[1]
        rotation_matrix[0, 2] += (t_x - eyes_center[0])
        rotation_matrix[1, 2] += (t_y - eyes_center[1])

        # Apply the affine transformation
        (w, h) = (self.desired_face_width, self.desired_face_height)
        output = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC)

        # ones = np.ones(shape=(len(shape), 1))
        # landmarks_one = np.hstack([shape, ones])
        # warped_landmarks = rotation_matrix.dot(landmarks_one.T).T
        #
        # transformed_landmarks = np.reshape(cv2.transform(np.expand_dims(shape, 1), rotation_matrix), (68, 2)).astype('int')
        transformed_landmarks = self.predictor.get_2d_landmarks(output)

        # Return the aligned face with new landmarks
        return output, transformed_landmarks


if __name__ == '__main__':
    aligner = FaceAligner()
