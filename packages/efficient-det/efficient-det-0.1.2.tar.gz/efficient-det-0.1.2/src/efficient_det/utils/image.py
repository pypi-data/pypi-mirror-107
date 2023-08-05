import cv2
import numpy as np


def normalize(image):
    """ Normalize image along channel axis.

    Args:
        image: Image array.

    Returns: Normalized image.

    """
    # std and mean are dataset specific
    std = [0.25472827, 0.25604966, 0.26684684]
    mean = [0.48652189, 0.50312634, 0.44743868]

    new_image = image / 255.
    new_image = (new_image - mean) / std

    return new_image


def resize_image(image, image_shape):
    """ Resize image taking into account aspect ratio.

    Args:
        image: Image to resize.
        image_shape: Size to which image will be scaled.

    Returns: Resized image.
    Resizing is inspired by
    https://github.com/huohuotm/EfficientDet-1/blob/master/generators/common.py

    """
    image_width = image.shape[1]
    image_height = image.shape[0]

    if image_height > image_width:
        scale = image_shape[0] / image_height
        resized_height = image_shape[0]
        resized_width = int(image_width * scale)
    else:
        scale = image_shape[1] / image_width
        resized_width = image_shape[1]
        resized_height = int(image_height * scale)

    image = cv2.resize(image, (resized_width, resized_height))
    new_image = np.ones(image_shape, dtype=np.float32) * 128

    offset_h = (image_shape[1] - resized_height) // 2
    offset_w = (image_shape[0] - resized_width) // 2

    height = offset_h + resized_height
    width = offset_w + resized_width

    new_image[offset_h:height, offset_w:width] = image

    return new_image, scale, offset_w, offset_h
