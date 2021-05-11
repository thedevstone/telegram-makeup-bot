import cv2
import numpy as np

from image_alterations_detector.face_morphology.landmarks_prediction.utils import FACIAL_LANDMARKS_INDEXES


def visualize_facial_landmarks_points(img: np.ndarray, landmarks_2d: np.ndarray) -> np.ndarray:
    """ Visualize facial landmark in the form of points

    :param img: the input image
    :param landmarks_2d: the landmark array
    :return: the new image with landmark visualization
    """
    img_out = np.array(img)
    for n in range(0, 68):
        x = landmarks_2d[n, 0]
        y = landmarks_2d[n, 1]
        cv2.circle(img_out, (x, y), 1, (0, 0, 255), -1)
    return img_out


def visualize_facial_landmarks_areas(image: np.ndarray, shape: np.ndarray, colors=None, alpha=0.75) -> np.ndarray:
    """ Visualization of facial landmarks_prediction with overlay

    :param image: the input image
    :param shape: the input shape
    :param colors: colors of face regions
    :param alpha: the alpha blending
    :return: the landmark visualization image
    """
    overlay = image.copy()
    output = image.copy()

    # Default coloring
    if colors is None:
        colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
                  (168, 100, 168), (158, 163, 32),
                  (163, 38, 32), (180, 42, 220), (150, 150, 255)]

    # For each landmark region
    for (i, name) in enumerate(FACIAL_LANDMARKS_INDEXES.keys()):
        (init, end) = FACIAL_LANDMARKS_INDEXES[name]
        landmarks = shape[init: end]

        # Since the jawline is a non-enclosed facial region, just draw lines between the (x, y)-coordinates
        if name == "jaw":
            for jaw_point in range(1, len(landmarks)):
                point_a = tuple(landmarks[jaw_point - 1])
                point_b = tuple(landmarks[jaw_point])
                cv2.line(overlay, point_a, point_b, colors[i], 2)
        # Otherwise, compute the convex hull of the facial landmark coordinates points and display it
        else:
            hull = cv2.convexHull(landmarks)
            cv2.drawContours(overlay, [hull], -1, colors[i], -1)

    # Apply the transparent overlay
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    # return the output image
    return output
