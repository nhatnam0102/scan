import os

import cv2
import numpy as np

from upc.common import general
from collections import OrderedDict
import shutil

import cv2

# Colors (B, G, R)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def create_blank(width, height, color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in BGR"""
    image = np.zeros((height, width, 3), np.uint8)
    # Fill image with color
    image[:] = color

    return image


def draw_half_circle_no_round(image):
    height, width = image.shape[0:2]
    # Ellipse parameters
    radius = 100
    center = (width / 2, height - 25)
    axes = (radius, radius)
    angle = 0
    startAngle = 180
    endAngle = 360
    # When thickness == -1 -> Fill shape
    thickness = -1

    # Draw black half circle
    cv2.ellipse(image, center, axes, angle, startAngle, endAngle, BLACK, thickness)

    axes = (radius - 10, radius - 10)
    # Draw a bit smaller white half circle
    cv2.ellipse(image, center, axes, angle, startAngle, endAngle, WHITE, thickness)
    cv2.e


draw_half_circle_no_round(create_blank(300,150))