import os

import cv2
from matplotlib import pyplot as plt

from face_alignment.face_aligner import FaceAligner
from file_manager.path_utilities import ROOT_DIR
from image_utils.loading import load_img
from makeup.makeup import hair
from segmentation.conversions import denormalize
from segmentation.face_segmenter import FaceSegmenter

if __name__ == '__main__':
    image = load_img('rez.jpg')
    # cap = cv2.VideoCapture(0)
    # ret, image = cap.read()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cap.release()

    # Align and segment
    face_aligner = FaceAligner(desired_face_width=int(image.shape[1] / 2))
    image, landmarks = face_aligner.align(image)
    plt.imshow(image)
    plt.show()
    face_segmenter = FaceSegmenter(512)
    segmented = face_segmenter.segment_image_keep_aspect_ratio(image)
    hair_mask = denormalize(segmented)[:, :, 6]

    # hair_mask = load_img_gray('hair_mask_luca.png')
    cv2.imwrite(os.path.join(ROOT_DIR, 'images', 'hair_mask_luca.png'), hair_mask)
    color =  [255, 26, 26]  # [255, 128, 128] # [50, 150, 50]
    changed_image = hair(image, hair_mask, color, dark_hair=False, force=0.3)
    plt.imshow(changed_image)
    plt.show()
