from typing import List

import cv2
import numpy as np

from image_utils.conversion import image_resize_with_border, image_resize_restore_ratio
from segmentation import conversions
from segmentation.configuration import color_configuration
from segmentation.configuration.keras_backend import set_keras_backend
from segmentation.lite_model import LiteModel

CLASSES_TO_SEGMENT = {'skin': True, 'nose': True, 'eye': True, 'brow': True, 'ear': True, 'mouth': True,
                      'hair': True, 'neck': True, 'cloth': False}


class FaceSegmenter:
    def __init__(self, image_size=256):
        set_keras_backend()
        # Configuration
        self.image_size = image_size
        # Load the model
        # from segmentation import model
        # self.inference_model = model.load_model(get_model_path('unet.h5'))
        # serialize_tflite_model(self.inference_model, self.image_size)
        self.lite_model = LiteModel('unet-{}.tflite'.format(self.image_size))

    def segment_image(self, img):
        img = cv2.resize(img, (self.image_size, self.image_size), cv2.INTER_LANCZOS4)
        img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2])).astype('float')
        img1_normalized = (img / 255.0).astype('float32')
        # images_predicted = self.inference_model(img1_normalized).numpy()
        images_predicted = self.lite_model.predict(img1_normalized)
        image_predicted = images_predicted[0]
        return image_predicted

    def segment_images(self, images: List[np.ndarray]):
        # Output images
        predicted_images = []
        # Images
        for img in images:
            predicted_images.append(self.segment_image(img))
        return predicted_images

    def segment_image_keep_aspect_ratio(self, img):
        resized, old_size, border = image_resize_with_border(img, size=self.image_size)
        segmented = self.segment_image(resized)
        restored = image_resize_restore_ratio(segmented, old_size, border)
        return restored

    def segment_images_keep_aspect_ratio(self, images: List[np.ndarray]):
        # Output images
        predicted_images = []
        # Images
        for img in images:
            predicted_images.append(self.segment_image_keep_aspect_ratio(img))
        return predicted_images


def denormalize_and_convert_rgb(masks):
    colors_values_list = color_configuration.get_classes_colors(CLASSES_TO_SEGMENT)
    rgb_images = []
    for mask in masks:
        img_rgb = conversions.denormalize(mask)
        img_rgb = conversions.mask_channels_to_rgb(img_rgb, 8, colors_values_list)
        rgb_images.append(img_rgb)
    return rgb_images
