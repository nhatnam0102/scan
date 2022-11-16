import time

import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from upc.common import style_sheet


class DetectWidget(QtWidgets.QWidget):
    def __init__(self):
        super(DetectWidget, self).__init__()
