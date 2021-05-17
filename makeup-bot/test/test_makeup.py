import os

import cv2
from matplotlib import pyplot as plt

from bot.conversation.makeup.utils import COLORS
from face_alignment.face_aligner import FaceAligner
from file_manager.path_utilities import ROOT_DIR
from image_utils.loading import load_img
from makeup.makeup import colorize, hair, lips
from segmentation.conversions import denormalize
from segmentation.face_segmenter import FaceSegmenter

if __name__ == '__main__':
    image = load_img('girl.jpg')
    # cap = cv2.VideoCapture(0)
    # ret, image = cap.read()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cap.release()

    # Align and segment
    face_aligner = FaceAligner()
    image, landmarks = face_aligner.align(image)
    face_segmenter = FaceSegmenter(256)
    masks = face_segmenter.segment_image_keep_aspect_ratio(image)

    color = COLORS['purple']
    hair_makeup_image = hair(image, masks, color, dark_hair=False, force=0.0)
    plt.imshow(hair_makeup_image)
    plt.show()
    lips_makeup_image = lips(image, masks, color, pronounced=False, force=0.0)
    plt.imshow(lips_makeup_image)
    plt.show()


