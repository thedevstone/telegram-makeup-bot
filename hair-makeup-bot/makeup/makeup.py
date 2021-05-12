import cv2
import numpy as np
from skimage.filters import gaussian

from segmentation.conversions import denormalize


def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, multichannel=True)

    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img

    img_out = img_out / 255.0

    mask_1 = img_out < 0
    mask_2 = img_out > 1

    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255
    return np.array(img_out, dtype=np.uint8)


def increase_brightness(hsv, value=30):
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    return final_hsv


def hair(image, masks: np.ndarray, color, dark_hair=False, force=0.1):
    hair_mask = denormalize(masks)[:, :, 6]
    return colorize(image, hair_mask, color, overlay=dark_hair, force=force)


def lips(image, masks: np.ndarray, color, pronounced=False, force=0.1):
    lips_mask = denormalize(masks)[:, :, 5]
    return colorize(image, lips_mask, color, overlay=pronounced, force=force)


def colorize(image, mask: np.ndarray, color, overlay=False, force=0.1):
    # Create color layer
    if overlay:
        colored_image = image.copy()
        colored_image[mask == 255] = color
        # Blend images together
        changed_img = cv2.addWeighted(colored_image, force, image, 1 - force, 0, colored_image)
        return changed_img
    else:
        out_image = image.copy()
        r, g, b = color
        color_mask = np.zeros_like(image)
        color_mask[:, :, 0] = r
        color_mask[:, :, 1] = g
        color_mask[:, :, 2] = b
        image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        color_mask_hsv = cv2.cvtColor(color_mask, cv2.COLOR_RGB2HSV)
        image_hsv[:, :, 0:1] = color_mask_hsv[:, :, 0:1]
        changed_img = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)
        out_image[mask == 255] = changed_img[mask == 255]
        return out_image
