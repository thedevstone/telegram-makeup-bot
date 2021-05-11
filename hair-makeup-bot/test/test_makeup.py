import os.path

import cv2
from matplotlib import pyplot as plt

from file_manager.path_utilities import ROOT_DIR
from image_utils.loading import load_img, load_img_gray
from makeup.makeup import hair
from segmentation.conversions import denormalize, mask_channels_to_rgb
from segmentation.face_segmenter import FaceSegmenter, denormalize_and_convert_rgb

if __name__ == '__main__':
    image = load_img('img.png')
    cap = cv2.VideoCapture(0)
    ret, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cap.release()
    face_segmenter = FaceSegmenter()
    segmented = face_segmenter.segment_image_keep_aspect_ratio(image)
    plt.imshow(denormalize_and_convert_rgb([segmented])[0])
    plt.show()
    hair_mask = denormalize(segmented)[:, :, 6]
    # hair_mask = load_img_gray('hair_mask.png')
    # cv2.imwrite(os.path.join(ROOT_DIR, 'images', 'hair_mask.png'), hair_mask)
    # denormalized = denormalize_and_convert_rgb([segmented])[0]
    color = [50, 150, 50]
    changed_image = hair(image, hair_mask, color, dark_hair=True, force=0.2)
    plt.imshow(changed_image)
    plt.show()
