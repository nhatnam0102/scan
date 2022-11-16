import time

import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from upc.common import style_sheet


class InitWidget(QtWidgets.QWidget):
    def __init__(self):
        super(InitWidget, self).__init__()
        intro_layout = QVBoxLayout()

        ai_logo = QtSvg.QSvgWidget("./assets/resource/ai.svg")
        loading_widget = QtWidgets.QWidget()
        loading_layout = QHBoxLayout()

        self.notification_init = QLabel("")
        self.notification_init.setStyleSheet(style_sheet.QLabelStyle(text_color=style_sheet.main_color, font_size=30))

        load2 = QtSvg.QSvgWidget("./assets/resource/200px.svg")
        loading_layout.addWidget(self.notification_init)
        loading_layout.addWidget(load2)
        loading_widget.setLayout(loading_layout)
        intro_layout.addWidget(ai_logo, 7, QtCore.Qt.AlignCenter)
        intro_layout.addWidget(loading_widget, 3, QtCore.Qt.AlignCenter)
        self.setLayout(intro_layout)
