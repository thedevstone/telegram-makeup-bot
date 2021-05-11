import os.path

import cv2
from matplotlib import pyplot as plt

from file_manager.path_utilities import ROOT_DIR
from image_utils.loading import load_img, load_img_gray
from makeup.makeup import hair

if __name__ == '__main__':
    image = load_img('img.png')
    # face_segmenter = FaceSegmenter()
    # segmented = face_segmenter.segment_image_keep_aspect_ratio(image)
    # hair_mask = segmented[:, :, 6]
    # hair_mask = hair_mask * 255.0
    # hair_mask.astype('uint8')
    hair_mask = load_img_gray('hair_mask.png')
    cv2.imwrite(os.path.join(ROOT_DIR, 'images', 'hair_mask.png'), hair_mask)
    # denormalized = denormalize_and_convert_rgb([segmented])[0]
    color = [50, 150, 50]
    changed_image = hair(image, hair_mask, color)
    plt.imshow(changed_image)
    plt.show()
