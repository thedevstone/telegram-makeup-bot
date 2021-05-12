import os

import cv2
from matplotlib import pyplot as plt

from face_alignment.face_aligner import FaceAligner
from file_manager.path_utilities import ROOT_DIR
from image_utils.loading import load_img
from makeup.makeup import colorize, hair, lips
from segmentation.conversions import denormalize
from segmentation.face_segmenter import FaceSegmenter

if __name__ == '__main__':
    image = load_img('franco3.png')
    # cap = cv2.VideoCapture(0)
    # ret, image = cap.read()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cap.release()

    # Align and segment
    face_aligner = FaceAligner(desired_face_width=int(image.shape[1] / 2))
    image, landmarks = face_aligner.align(image)
    face_segmenter = FaceSegmenter(512)
    masks = face_segmenter.segment_image_keep_aspect_ratio(image)

    color = [26, 26, 255] # [255, 26, 26]  # [255, 128, 128] # [50, 150, 50]
    hair_makeup_image = hair(image, masks, color, dark_hair=False, force=0.2)
    plt.imshow(hair_makeup_image)
    plt.show()
    lips_makeup_image = lips(image, masks, color, pronounced=True, force=0.2)
    plt.imshow(lips_makeup_image)
    plt.show()


