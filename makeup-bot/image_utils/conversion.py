import cv2


def image_resize_with_border(img, size=512):
    old_size = img.shape[:2]
    ratio = float(size) / max(old_size)
    new_size = tuple([round(x * ratio) for x in old_size])
    im = cv2.resize(img, (new_size[1], new_size[0]), cv2.INTER_LANCZOS4)
    delta_w = size - new_size[1]
    delta_h = size - new_size[0]
    mid_border_y = delta_h // 2
    mid_border_x = delta_w // 2
    top, bottom = mid_border_y, delta_h - mid_border_y
    left, right = mid_border_x, delta_w - mid_border_x
    color = [0, 0, 0]
    new_img = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return new_img, old_size, (top, bottom, left, right)


def image_resize_restore_ratio(img, new_size, border):
    crop_img = img[border[0]: img.shape[0] - border[1], border[2]: img.shape[1] - border[3]]
    restored_img = cv2.resize(crop_img, (new_size[1], new_size[0]), cv2.INTER_LANCZOS4)
    return restored_img
