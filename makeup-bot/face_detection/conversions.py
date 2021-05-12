def rect_to_bounding_box(rect):
    """
    Take a bounding predicted by dlib and convert it to the format (x, y, w, h) as we would normally do with OpenCV

    :param rect: the bounding rect
    :return: (x, y, w, h) coordinate of the bounding box
    """
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return x, y, w, h
