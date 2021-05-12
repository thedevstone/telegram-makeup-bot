import numpy as np


def landmarks_to_array(shape, dtype="int"):
    """
    Convert dlib landmark notation to numpy array of tuple

    :param shape: the landmark shape
    :param dtype: the type of output matrix
    :return: the numpy of tuple conversion
    """
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)
    # loop over the 68 facial landmarks_prediction and convert them to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords
