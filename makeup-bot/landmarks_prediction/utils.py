# import the necessary packages
from collections import OrderedDict

import numpy as np

# Define a dictionary that maps the indexes of the facial landmarks_prediction to specific face regions
# For dlib’s 68-point facial landmark detector:
FACIAL_LANDMARKS_68_INDEXES = OrderedDict([
    ("mouth", (48, 68)),
    ("inner_mouth", (60, 68)),
    ("right_eyebrow", (17, 22)),
    ("left_eyebrow", (22, 27)),
    ("right_eye", (36, 42)),
    ("left_eye", (42, 48)),
    ("nose", (27, 36)),
    ("jaw", (0, 17))
])

# For dlib’s 5-point facial landmark detector:
FACIAL_LANDMARKS_5_INDEXES = OrderedDict([
    ("right_eye", (2, 3)),
    ("left_eye", (0, 1)),
    ("nose", 4)
])

# in order to support legacy code, we'll default the indexes to the
# 68-point model
FACIAL_LANDMARKS_INDEXES = FACIAL_LANDMARKS_68_INDEXES


def get_indexes_group_from_key(indexes_group_key: str) -> np.ndarray:
    """ Get a group of indexes in the form of numpy array

    :param indexes_group_key the key in the FACIAL-LANDMARK dictionary
    :return: the numpy array of indexes
    """
    start, stop = FACIAL_LANDMARKS_68_INDEXES[indexes_group_key]
    return np.arange(start, stop)
