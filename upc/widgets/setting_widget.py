import time

import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from upc.common import style_sheet, general

import configparser as cp


class SettingWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SettingWidget, self).__init__()
        self.u_cloud_url = None
        self.rpa_qr = None
        self.yk_center = None
        self.side_focus = None
        self.iou = None
        self.conf = None
        self.top_focus = None
        self.load_config()
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()

        center_widget = QGroupBox()
        general.set_shadow(center_widget)
        center_widget.setStyleSheet(style_sheet.QGroupBoxStyle2())
        center_widget.setMinimumWidth(1500)
        center_layout = QGridLayout()

        lb_U_cloud = QLabel("U- CLoud ")
        lb_U_cloud.setStyleSheet(style_sheet.QLabelStyle())
        self.u_cloud_url = QLineEdit("upc.co.jp")
        self.u_cloud_url.setAlignment(QtCore.Qt.AlignCenter)
        self.u_cloud_url.setStyleSheet(style_sheet.QLineEditStyle())

        lb_yk_center = QLabel("利用センター")
        lb_yk_center.setStyleSheet(style_sheet.QLabelStyle())
        self.yk_center = QComboBox()
        self.yk_center.addItems(['東京 センター', 'ベトナムセンター', '中国センター'])
        self.yk_center.setStyleSheet(style_sheet.QComboBoxStyle())

        lb_rpa_qr = QLabel("RPA/QR")
        lb_rpa_qr.setStyleSheet(style_sheet.QLabelStyle())
        self.rpa_qr = QComboBox()
        self.rpa_qr.addItems(['RPA', 'QR', 'RPA/QR'])
        self.rpa_qr.setStyleSheet(style_sheet.QComboBoxStyle())

        lb_printer = QLabel("プリンター")
        lb_printer.setStyleSheet(style_sheet.QLabelStyle())
        self.printer = QComboBox()
        self.printer.addItems(['POS-80', 'POS-58', 'USB プリンター'])
        self.printer.setStyleSheet(style_sheet.QComboBoxStyle())

        lb_iou = QLabel("IOU")
        lb_iou.setStyleSheet(style_sheet.QLabelStyle())
        self.iou = QLineEdit(str(self.iou))
        self.iou.setAlignment(QtCore.Qt.AlignCenter)
        self.iou.setStyleSheet(style_sheet.QLineEditStyle())

        lb_focus_top = QLabel("上フォーカス　")
        lb_focus_top.setStyleSheet(style_sheet.QLabelStyle())
        self.focus_top = QLineEdit(str(self.top_focus))
        self.focus_top.setAlignment(QtCore.Qt.AlignCenter)
        self.focus_top.setStyleSheet(style_sheet.QLineEditStyle())

        lb_focus_side = QLabel("横フォーカス　")
        lb_focus_side.setStyleSheet(style_sheet.QLabelStyle())
        self.focus_side = QLineEdit(str(self.side_focus))
        self.focus_side.setAlignment(QtCore.Qt.AlignCenter)
        self.focus_side.setStyleSheet(style_sheet.QLineEditStyle())

        lb_conf = QLabel("Confidence")
        lb_conf.setStyleSheet(style_sheet.QLabelStyle())
        self.conf = QLineEdit(str(self.conf))
        self.conf.setAlignment(QtCore.Qt.AlignCenter)
        self.conf.setStyleSheet(style_sheet.QLineEditStyle())

        center_layout.setSpacing(50)

        center_layout.addWidget(lb_U_cloud, 1, 1, )
        center_layout.addWidget(self.u_cloud_url, 1, 2)

        center_layout.addWidget(lb_iou, 1, 3, )
        center_layout.addWidget(self.iou, 1, 4, )

        center_layout.addWidget(lb_yk_center, 2, 1, )
        center_layout.addWidget(self.yk_center, 2, 2, )

        center_layout.addWidget(lb_conf, 2, 3, )
        center_layout.addWidget(self.conf, 2, 4, )

        center_layout.addWidget(lb_rpa_qr, 3, 1, )
        center_layout.addWidget(self.rpa_qr, 3, 2, )

        center_layout.addWidget(lb_focus_top, 3, 3, )
        center_layout.addWidget(self.focus_top, 3, 4, )

        center_layout.addWidget(lb_printer, 4, 1, )
        center_layout.addWidget(self.printer, 4, 2, )

        center_layout.addWidget(lb_focus_side, 4, 3, )
        center_layout.addWidget(self.focus_side, 4, 4, )

        center_widget.setLayout(center_layout)

        bottom_widget = QtWidgets.QWidget()
        bottom_layout = QHBoxLayout()

        self.btn_back = QToolButton()
        self.btn_back.setText("戻る")
        self.btn_back.setStyleSheet(style_sheet.QToolButtonStyle())
        general.set_shadow(self.btn_back)

        self.btn_save = QToolButton()
        self.btn_save.setText("登録")
        self.btn_save.setStyleSheet(style_sheet.QToolButtonStyle())
        general.set_shadow(self.btn_save)

        bottom_layout.addWidget(self.btn_back)
        bottom_layout.addWidget(self.btn_save)

        bottom_widget.setLayout(bottom_layout)

        main_layout.addWidget(center_widget, 8, Qt.AlignHCenter)
        main_layout.addWidget(bottom_widget, 2, Qt.AlignHCenter)

        self.setLayout(main_layout)

    def load_config(self):
        config = cp.ConfigParser()
        config.read(os.path.join(os.getcwd(), "upc", "common", "config.ini"), encoding='UTF-8')
        self.iou = config["model"]["iou"]
        self.conf = config["model"]["conf"]
        self.top_focus = config["camera"]["top_focus"]
        self.side_focus = config["camera"]["side_focus"]
        self.yk_center = config["yk"]["yk_center"]
        self.rpa_qr = config["yk"]["rpa_qr"]
        # self.agnostic=config['model'].getboolean('agnostic')
