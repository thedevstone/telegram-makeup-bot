from typing import List

import numpy as np


def denormalize(image: np.ndarray) -> np.ndarray:
    """ Denormalize 'float32' image in [0,1] to 'uint8' image in [0,255]

    :param image the input image
    """
    if image.dtype == 'uint8':
        raise ValueError('Cannot denormalize already uint8 image')
    return (image * 255.).astype('uint8')


def mask_channels_to_rgb(image: np.ndarray,
                         n_classes: int,
                         colors_values_list: List[np.ndarray]) -> np.ndarray:
    """ Convert denormalized image 'uint8' [0,255] to RGB image [0,255]

    :param image: the n-classes-depth input image
    :param n_classes: the depth of the image
    :param image_size: the image size
    :param colors_values_list: the list of conversion colors
    :return: the converted rgb image
    """
    channels = np.dsplit(image, n_classes + 1)
    width, height = image.shape[:2]
    rgb_out_image = np.zeros((width, height, 3))
    # Iterate over binary masks and applying color to rgb image only in corresponding foreground pixels in masks
    for idx, color in enumerate(colors_values_list):
        indexing = np.reshape(channels[idx], (width, height))
        indexing = indexing > 128  # Foreground
        rgb_out_image[indexing] = color
    # applying color to rgb image only in corresponding foreground pixels of background mask
    indexing = np.reshape(channels[-1], (width, height))
    indexing = indexing > 128
    rgb_out_image[indexing] = [0, 0, 0]
    return rgb_out_image.astype('uint8')
