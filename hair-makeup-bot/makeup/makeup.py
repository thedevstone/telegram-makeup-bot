import cv2
import numpy as np
from skimage.filters import gaussian


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


def hair(image, mask: np.ndarray, color, dark_hair=False, force=0.1):
    # Create color layer
    if dark_hair:
        colored_image = image.copy()
        colored_image[mask == 255] = color
        # Blend images together
        changed_img = cv2.addWeighted(colored_image, force, image, 1 - force, 0, colored_image)
        return changed_img
    else:
        out_image = image.copy()
        b, g, r = color
        color_mask = np.zeros_like(image)
        color_mask[:, :, 0] = b
        color_mask[:, :, 1] = g
        color_mask[:, :, 2] = r
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        color_mask_hsv = cv2.cvtColor(color_mask, cv2.COLOR_BGR2HSV)
        image_hsv[:, :, 0:1] = color_mask_hsv[:, :, 0:1]
        changed_img = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
        out_image[mask == 255] = changed_img[mask == 255]
        return out_image
