import cv2

from image_utils.loading import load_img
from segmentation.face_segmenter import FaceSegmenter, denormalize_and_convert_rgb

if __name__ == '__main__':
    face_segmenter = FaceSegmenter()
    image = load_img('franco2.png')
    segmented = face_segmenter.segment_image_keep_aspect_ratio(image)
    denormalized = denormalize_and_convert_rgb([segmented])[0]
    cv2.imshow('segmented', denormalized)
    cv2.waitKey()
