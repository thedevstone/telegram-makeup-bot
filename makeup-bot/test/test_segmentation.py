import cv2
import matplotlib.pyplot as plt

from face_alignment.face_aligner import FaceAligner
from image_utils.loading import load_img
from segmentation.face_segmenter import FaceSegmenter, denormalize_and_convert_rgb

if __name__ == '__main__':
    face_segmenter = FaceSegmenter(256)
    image = load_img('franco2.png')
    # cap = cv2.VideoCapture(0)
    # ret, image = cap.read()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cap.release()

    # Align and segment
    face_aligner = FaceAligner(desired_face_width=256)
    image, landmarks = face_aligner.align(image)
    plt.imshow(image)
    plt.show()
    segmented = face_segmenter.segment_image_keep_aspect_ratio(image)
    denormalized = denormalize_and_convert_rgb([segmented])[0]
    plt.imshow(denormalized)
    plt.show()
