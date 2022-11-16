import time

import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from upc.common import style_sheet, general
from upc.widgets.ai_detect_widget import AiDetectWidget
import threading


class ActionWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ActionWidget, self).__init__()
        self.rpa_qr = None
        self.camera_loaded = None
        self.lb_yl_name = None
        self.lb_yl_id = None
        self.lb_center = None
        self.action_1 = None
        self.setContentsMargins(0, 0, 0, 0)
        try:
            self.create_ui()
        except Exception as e:
            print(e)
        self.ai_detect_widget = AiDetectWidget()

    def create_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        information_widget = QGroupBox()
        information_widget.setStyleSheet(style_sheet.QGroupBoxHeader())
        information_layout = QHBoxLayout()
        general.set_shadow(information_widget)
        self.lb_center = QLabel()
        self.lb_center.setStyleSheet(style_sheet.QLabelStyle(font_size=30))

        yl_widget = QtWidgets.QWidget()
        yl_layout = QHBoxLayout()
        lb_yl_id = QLabel("担当者CD")
        lb_yl_id.setStyleSheet(style_sheet.QLabelStyle())

        self.lb_yl_id = QLabel()
        self.lb_yl_id.setMinimumSize(300, 50)
        self.lb_yl_id.setStyleSheet(style_sheet.QLabelStyle_1(font_size=30, background_color="white"))
        self.lb_yl_id.setAlignment(QtCore.Qt.AlignCenter)
        yl_layout.addWidget(lb_yl_id)
        yl_layout.addWidget(self.lb_yl_id)
        yl_widget.setLayout(yl_layout)

        yl_name_widget = QtWidgets.QWidget()
        yl_name_layout = QHBoxLayout()
        lb_yl_name = QLabel("担当者名")
        lb_yl_name.setStyleSheet(style_sheet.QLabelStyle())

        self.lb_yl_name = QLabel()
        self.lb_yl_name.setMinimumSize(300, 50)
        self.lb_yl_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_yl_name.setStyleSheet(style_sheet.QLabelStyle_1(font_size=30, background_color="white"))
        yl_name_layout.addWidget(lb_yl_name)
        yl_name_layout.addWidget(self.lb_yl_name)
        yl_name_widget.setLayout(yl_name_layout)

        self.rpa_qr = QLabel()
        self.rpa_qr.setStyleSheet(style_sheet.QLabelStyle(font_size=30, text_color="white"))

        information_layout.addWidget(self.lb_center, 4, QtCore.Qt.AlignLeft)
        information_layout.addWidget(yl_widget, 2, Qt.AlignRight)
        information_layout.addWidget(yl_name_widget, 3, Qt.AlignRight)
        information_layout.addWidget(self.rpa_qr, 1, Qt.AlignRight)

        information_widget.setLayout(information_layout)

        action_widget = QtWidgets.QWidget()
        action_layout = QGridLayout()

        self.action_1 = QToolButton()
        general.set_shadow(self.action_1)
        self.action_1.setText("YL仕入")
        self.action_1.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_2 = QToolButton()
        general.set_shadow(self.action_2)
        self.action_2.setText("マイナスYL仕入")
        self.action_2.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_3 = QToolButton()
        general.set_shadow(self.action_3)
        self.action_3.setText("ファミリー")
        self.action_3.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_4 = QToolButton()
        general.set_shadow(self.action_4)
        self.action_4.setText("移動出庫")
        self.action_4.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_5 = QToolButton()
        general.set_shadow(self.action_5)
        self.action_5.setText("移動入庫")
        self.action_5.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_6 = QToolButton()
        general.set_shadow(self.action_6)
        # self.action_6.setText(f'他勘定- 宣伝')
        general.set_text(self.action_6, text1="他勘定-", text2="宣伝")
        self.action_6.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_7 = QToolButton()
        general.set_shadow(self.action_7)
        # self.action_7.setText("他勘定-贈呈")
        general.set_text(self.action_7, text1="他勘定-", text2="贈呈")
        self.action_7.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_8 = QToolButton()
        general.set_shadow(self.action_8)
        # self.action_8.setText("他勘定-会議")
        general.set_text(self.action_8, text1="他勘定-", text2="会議")
        self.action_8.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_9 = QToolButton()
        general.set_shadow(self.action_9)
        # self.action_9.setText("他勘定-福利")
        general.set_text(self.action_9, text1="他勘定-", text2="福利")
        self.action_9.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_10 = QToolButton()
        general.set_shadow(self.action_10)
        # self.action_10.setText("他勘定-不良")
        general.set_text(self.action_10, text1="他勘定-", text2="不良")
        self.action_10.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_11 = QToolButton()
        general.set_shadow(self.action_11)
        # self.action_11.setText("他勘定-破損")
        general.set_text(self.action_11, text1="他勘定-", text2="破損")
        self.action_11.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_12 = QToolButton()
        general.set_shadow(self.action_12)
        # self.action_12.setText("他勘定-廃棄")
        general.set_text(self.action_12, text1="他勘定-", text2="廃棄")
        self.action_12.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        action_layout.setSpacing(60)
        action_layout.addWidget(self.action_1, 1, 1)
        action_layout.addWidget(self.action_2, 1, 2)
        action_layout.addWidget(self.action_3, 1, 3)
        action_layout.addWidget(self.action_4, 2, 1)
        action_layout.addWidget(self.action_5, 2, 2)
        action_layout.addWidget(self.action_6, 3, 1)
        action_layout.addWidget(self.action_7, 3, 2)
        action_layout.addWidget(self.action_8, 3, 3)
        action_layout.addWidget(self.action_9, 3, 4)
        action_layout.addWidget(self.action_10, 4, 1)
        action_layout.addWidget(self.action_11, 4, 2)
        action_layout.addWidget(self.action_12, 4, 3)

        action_widget.setLayout(action_layout)

        bottom_widget = QtWidgets.QWidget()
        bottom_layout = QHBoxLayout()

        self.back = QToolButton()
        general.set_shadow(self.back)
        self.back.setMaximumSize(300, 100)
        self.back.setText("戻る")

        self.back.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.com = QComboBox()
        self.com.setMaximumWidth(1000)
        self.com.setStyleSheet(style_sheet.QComboBoxStyle(height=100, border_radius=15))

        self.next = QToolButton()
        general.set_shadow(self.next)
        self.next.setMaximumSize(300, 100)
        self.next.setText("次へ")
        self.next.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        bottom_layout.addWidget(self.back)
        bottom_layout.addWidget(self.com)
        bottom_layout.addWidget(self.next)

        bottom_widget.setLayout(bottom_layout)

        main_layout.addWidget(information_widget, 2, QtCore.Qt.AlignTop)
        main_layout.addWidget(action_widget, 6, QtCore.Qt.AlignTop)
        main_layout.addWidget(bottom_widget, 2, QtCore.Qt.AlignTop)
        self.setLayout(main_layout)
