import cv2
import matplotlib.pyplot as plt

from image_utils.loading import load_img
from segmentation.face_segmenter import FaceSegmenter, denormalize_and_convert_rgb

if __name__ == '__main__':
    face_segmenter = FaceSegmenter()
    image = load_img('franco2.png')
    cap = cv2.VideoCapture(0)
    ret, image = cap.read()
    cap.release()
    segmented = face_segmenter.segment_image_keep_aspect_ratio(image)
    denormalized = denormalize_and_convert_rgb([segmented])[0]
    plt.imshow(denormalized)
    plt.show()
