import threading
import cv2

from PyQt5 import QtCore, QtWidgets, QtSvg
from PyQt5.QtGui import QRadialGradient, QGradient, QLinearGradient, QPen, QIcon
from PyQt5.QtWidgets import *
from upc.common import style_sheet, general
from upc.common.general import LOGGER
from upc.widgets.OutLineLabel import OutlinedLabel


class ScanAndSettingWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ScanAndSettingWidget, self).__init__()
        self.btn_exit = None
        self.btn_connect = None
        self.btn_setting = None
        self.notification = None
        self.btn_reload_camera = None
        self.is_loaded = False
        self.data_read = None
        self.setContentsMargins(0, 0, 0, 0)
        self.camera_list = None
        self.camera_loaded = {'TOP': 1, 'SIDE': 0}
        try:
            self.create_ui()
        except Exception as e:
            print(e)

    def create_ui(self):
        intro_layout = QVBoxLayout()
        # logo = QLabel(
        #     f'<font color={style_sheet.main_color}>YL</font>カードの<font color={style_sheet.main_color}>QR</font>を、<font '
        #     f'color={style_sheet.main_color}>上カメラ</font>にかざしてください。')
        # effect = QGraphicsDropShadowEffect()
        # effect.setOffset(-2, -1)
        # effect.setColor(QtCore.Qt.white)
        # logo.setGraphicsEffect(effect)
        try:
            logo = OutlinedLabel("YLカードのQRを、上カメラにかざしてください")
            logo.setOutlineThickness(1 / 8)
            # linearGrad = QLinearGradient(0, 1, 0, 0)
            # linearGrad.setCoordinateMode(QGradient.ObjectBoundingMode)
            # linearGrad.setStart(0, 0)
            # linearGrad.setFinalStop(1, 0)
            # linearGrad.setColorAt(0, QtCore.Qt.white)
            # linearGrad.setColorAt(1, QtCore.Qt.gray)
            # logo.setPen(QPen(linearGrad, 1))  # pen width is ignored
            logo.setStyleSheet('font-family:  Comic Sans MS; font-size: 60pt;')
        except Exception as e:
            print(e)

        # logo.setStyleSheet(style_sheet.QLabelStyle(font_size=50))

        self.btn_reload_camera = QToolButton()
        self.btn_reload_camera.setIcon((QIcon('./assets/resource/refresh.png')))
        self.btn_reload_camera.setMaximumHeight(50)
        self.btn_reload_camera.setStyleSheet(
            style_sheet.QToolButtonStyle(width=50, height=50, background_color="transparent",padding_top=0,
                                         background_color_hover="transparent"))

        notification_widget = QtWidgets.QWidget()
        notification_layout = QHBoxLayout()
        self.notification = QLabel("")
        self.notification.setStyleSheet(style_sheet.QLabelStyle(font_size=50, text_color="red"))
        # try:
        #
        #     self.notification = OutlinedLabel("")
        #     self.notification.setBrush(QtCore.Qt.red)
        #     self.notification.setOutlineThickness(1 / 8)
        #     self.notification.setStyleSheet('font-family:  Comic Sans MS; font-size: 40pt;')
        # except Exception as e:
        #     print(e)

        notification_layout.addWidget(self.notification)
        notification_widget.setLayout(notification_layout)

        loading = QtSvg.QSvgWidget("./assets/resource/load1.svg")

        setting_widget = QtWidgets.QWidget()
        setting_layout = QHBoxLayout()
        self.btn_setting = QToolButton()
        general.set_shadow(self.btn_setting)
        self.btn_setting.setText("SETTING")
        self.btn_setting.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.btn_connect = QToolButton()
        general.set_shadow(self.btn_connect)
        self.btn_connect.setText("CONNECT")
        self.btn_connect.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.btn_exit = QToolButton()
        general.set_shadow(self.btn_exit)
        self.btn_exit.setText("EXIT")
        self.btn_exit.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        setting_layout.addWidget(self.btn_setting)
        setting_layout.addWidget(self.btn_connect)
        setting_layout.addWidget(self.btn_exit)
        setting_widget.setLayout(setting_layout)

        intro_layout.addWidget(logo, 2, QtCore.Qt.AlignCenter)
        intro_layout.addWidget(self.btn_reload_camera, 1, QtCore.Qt.AlignCenter)
        intro_layout.addWidget(notification_widget, 1, QtCore.Qt.AlignCenter)
        intro_layout.addWidget(loading, 3, QtCore.Qt.AlignCenter)
        intro_layout.addWidget(setting_widget, 3, QtCore.Qt.AlignCenter)
        self.setLayout(intro_layout)

    def load_camera_thread(self):
        self.is_loaded = False
        camera_list = general.load_camera()
        self.is_loaded = True
        if len(camera_list) != 2:
            return
        elif len(camera_list) == 2:
            self.camera_list = camera_list
            self.scan_barcode()

    def load_list_camera(self, is_reload=False):
        self.camera_list = None
        if is_reload:
            t = threading.Thread(target=self.load_camera_thread)
            t.start()
        else:
            camera_list = general.load_camera()
            if camera_list is not None:
                self.camera_list = camera_list
            if len(camera_list) < 2:
                return
            self.scan_barcode()

    def scan_barcode(self):
        self.data_read = None
        if len(self.camera_list) == 2:
            t1 = threading.Thread(target=self.open_camera_event, args=[int(self.camera_list[0])])
            t2 = threading.Thread(target=self.open_camera_event, args=[int(self.camera_list[1])])
            t1.start()
            t2.start()

    def open_camera_event(self, camera_source):
        try:
            cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
            detector = cv2.QRCodeDetector()
            while True:
                r, frame = cap.read()
                if not r:
                    cap.release()
                    break

                data, bbox, _ = detector.detectAndDecode(frame)
                if data:
                    self.data_read = data
                    if camera_source == 0:
                        self.camera_loaded["SIDE"] = 1
                        self.camera_loaded["TOP"] = 0
                    else:
                        self.camera_loaded["SIDE"] = 0
                        self.camera_loaded["TOP"] = 1
                    break
                if self.data_read is not None:
                    LOGGER.info(f"Barcode data : {self.data_read}  Camera Loaded : {self.camera_loaded}")
                    break
        except Exception as e:
            LOGGER.error(e)
            return
