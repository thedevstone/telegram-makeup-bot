import cv2
from matplotlib import pyplot as plt

from bot.conversation.makeup.utils import COLORS
from image_utils.loading import load_img
from makeup.makeup import hair, lips
from segmentation.face_segmenter import FaceSegmenter

if __name__ == '__main__':
    image = load_img('girl.jpeg')
    # cap = cv2.VideoCapture(0)
    # ret, image = cap.read()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cap.release()

    # Align and segment
    # face_aligner = FaceAligner(desired_face_width=512)
    # image, landmarks = face_aligner.align(image)
    face_segmenter = FaceSegmenter(512)
    masks = face_segmenter.segment_image_keep_aspect_ratio(image)

    color = COLORS['purple']
    hair_makeup_image = hair(image, masks, color, dark_hair=False, force=0.0)
    hair_makeup_image = cv2.cvtColor(hair_makeup_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('../../readme-images/girl_hair.jpeg', hair_makeup_image)
    plt.imshow(hair_makeup_image)
    plt.show()
    lips_makeup_image = lips(image, masks, color, pronounced=False, force=0.0)
    lips_makeup_image = cv2.cvtColor(lips_makeup_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('../../readme-images/girl_lips.jpeg', lips_makeup_image)
    plt.imshow(lips_makeup_image)
    plt.show()
