from itertools import compress
from typing import List, Dict

import matplotlib.pyplot as plt
import numpy as np

SEGMENTATION_COLORS = {'blue': [0, 0, 204], 'green': [0, 153, 76], 'water': [0, 204, 204], 'orange': [255, 51, 51],
                       'purple': [204, 0, 204], 'yellow': [255, 255, 0], 'lilla': [204, 204, 255],
                       'dark_blue': [0, 51, 102],
                       'blue2': [0, 0, 255], 'light_green': [0, 204, 102], 'light_blue': [0, 255, 255],
                       'red': [204, 0, 0],
                       'violet': [153, 51, 255], 'dark_green': [0, 60, 0], 'brown': [150, 75, 0]}

CLASS_TO_SEGMENTATION_COLOR = {'skin': 'blue', 'nose': 'green', 'eye': 'violet', 'brow': 'brown', 'ear': 'yellow',
                               'mouth': 'red',
                               'hair': 'orange', 'neck': 'light_blue', 'cloth': 'purple'}


def get_classes_list(classes_to_segment: Dict[str, bool]) -> List[str]:
    classes_to_segment_boolean_indexing = list(classes_to_segment.values())
    classes_list = list(compress(classes_to_segment, classes_to_segment_boolean_indexing))
    return classes_list


def get_classes_colors(classes_to_segment: Dict[str, bool]) -> List[np.ndarray]:
    """ Get a configuration of classes to segment and return the corresponding colors

    :param classes_to_segment: the classes configuration
    :return: a tuple of list of classes and colors
    """
    classes_to_segment_boolean_indexing = list(classes_to_segment.values())
    classes_list = list(compress(classes_to_segment, classes_to_segment_boolean_indexing))
    colors_list = [CLASS_TO_SEGMENTATION_COLOR.get(key) for key in classes_list]
    colors_values_list = [SEGMENTATION_COLORS.get(key) for key in colors_list]

    return colors_values_list


def visualize_color_configuration(classes_to_segment: Dict[str, bool]) -> plt.Figure:
    """ Visualize color configuration

    :param classes_to_segment: the classes configuration
    :return: the configuration image
    """
    classes_list, colors_values_list = get_classes_colors(classes_to_segment)

    figure_colors: plt.Figure = plt.figure(figsize=(20, 4))
    plt.suptitle("Class to color", fontsize=30)

    for idx, elem in enumerate(zip(classes_list, colors_values_list)):
        ax_image = figure_colors.add_subplot(1, len(classes_list), idx + 1)
        ax_image.axis('off')
        ax_image.set_title(elem[0], fontsize=20)
        plt.imshow(np.full((50, 50, 3), elem[1], dtype='uint8'))
    return figure_colors
