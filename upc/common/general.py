from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import logging
from logging import *
from upc.common import style_sheet
import os


def get_all_file(path_dir):
    file_list, dir_list = [], []
    for rdir, subdir, files in os.walk(path_dir):
        file_list.extend([os.path.join(rdir, f) for f in files])
        dir_list.extend([os.path.join(rdir, d) for d in subdir])
    return file_list, dir_list


def set_logging(log_name,
                file_log_name,
                formatter="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    # Format with pathname and lineno
    # formatter=Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] %(message)s]')

    # Save log to file
    # f_handler = FileHandler(join(os.getcwd(), "data", "log", file_log_name))
    # f_handler.setLevel(logging.INFO)
    # f_handler.setFormatter(Formatter(formatter))
    # logger.addHandler(f_handler)

    # Show log in terminal(for DEBUG)
    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.INFO)
    s_handler.setFormatter(Formatter(formatter))

    logger.addHandler(s_handler)

    return logger


# LOGGER
LOGGER = set_logging("AI DETECT APP", "mylog.log")


def get_pixmap(resize, image):
    img = cv2.resize(image.getDrawImage(), (0, 0), fx=resize / image.getImage().shape[1],
                     fy=resize / image.getDrawImage().shape[1])
    img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(img)
    return pixmap


def set_shadow(widget, blur_radius=20, offset=3):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setColor(Qt.lightGray)
    shadow.setOffset(3)
    widget.setGraphicsEffect(shadow)


def set_opacity_on(widget, opacity_value: float = 1):
    opacity = QGraphicsOpacityEffect()
    opacity.setOpacity(opacity_value)
    widget.setGraphicsEffect(opacity)
    widget.setEnabled(True)


def set_opacity_off(widget, opacity=0):
    opacity_effect = QGraphicsOpacityEffect()
    opacity_effect.setOpacity(opacity)
    widget.setGraphicsEffect(opacity_effect)
    widget.setEnabled(False)


def show_message_dialog1(text):
    try:
        dlg = QDialog()
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        dlg.setWindowTitle("報告")
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        dlg.setStyleSheet("border-radius:10px;")
        dlg_layout = QVBoxLayout()

        wd = QGroupBox()
        # set_opacity_on(wd, opacity_value=opacity)
        wd.setStyleSheet(style_sheet.QGroupBoxStyle1())
        wd_layout = QVBoxLayout()

        mes = QLabel(text)
        btn_close = QDialogButtonBox.Close
        dlg.btnBox = QDialogButtonBox(btn_close)
        dlg.btnBox.setMaximumSize(70, 40)
        dlg.btnBox.button(QDialogButtonBox.Close).setText("閉じる")
        dlg.btnBox.setStyleSheet(style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))
        set_shadow(dlg.btnBox)

        dlg.btnBox.rejected.connect(dlg.close)
        wd_layout.addWidget(mes, 0, QtCore.Qt.AlignCenter)
        wd_layout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)
        wd.setLayout(wd_layout)
        dlg_layout.addWidget(wd)
        dlg.setLayout(dlg_layout)
        dlg.exec()
    except Exception as e:
        print(e)


def show_message_dialog(text, OK="OK", Cancel="取消"):
    try:
        dlg = QDialog()
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout()
        dlg_widget = QGroupBox("報告")
        dlg_widget.setStyleSheet(style_sheet.QGroupBoxStyle1(border_width=2))
        dlg_layout = QVBoxLayout()
        mes = QLabel(text)
        mes.setStyleSheet(style_sheet.QLabelStyle())
        btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dlg.btnBox = QDialogButtonBox(btn)
        dlg.btnBox.button(QDialogButtonBox.Cancel).setText(Cancel)
        dlg.btnBox.button(QDialogButtonBox.Ok).setText(OK)
        dlg.btnBox.setStyleSheet(style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))
        set_shadow(dlg.btnBox)

        dlg.btnBox.rejected.connect(dlg.reject)
        dlg.btnBox.accepted.connect(dlg.accept)
        dlg_layout.addWidget(QLabel(""), 0, QtCore.Qt.AlignCenter)
        dlg_layout.addWidget(mes, 0, QtCore.Qt.AlignCenter)
        dlg_layout.addWidget(QLabel("―――――――――――――――――――――"), 0, QtCore.Qt.AlignCenter)
        dlg_layout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)

        dlg_widget.setLayout(dlg_layout)

        layout.addWidget(dlg_widget)
        dlg.setLayout(layout)
        if dlg.exec():
            return True
        else:
            return False
    except Exception as e:
        print(e)


def load_camera():
    arr = [0,2]
    # res = 3000
    # for idx in range(0, 5, 1):
    #     cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, res)
    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH, res)
    #
    #     h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #     w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    #     arr.append(str(idx)) if int(h) not in [res, 0] else arr
    # LOGGER.info('Camera index available :  ' + ', '.join(f'{x}' for x in arr))
    return arr


# 他勘定 宣伝
def set_text(button, font_size1=5, font_size2=20, color1="#000000", color2="#000000", text1="", text2=""):
    text = QtGui.QTextDocument()
    text.setHtml(
        f'<b><font color={color1} size="{str(font_size1)}">{text1}</font> <font color={color2} size="{str(font_size2)}">{text2}</font></b>')
    pixmap = QtGui.QPixmap(text.size().toSize())
    pixmap.fill(QtCore.Qt.transparent)

    painter = QtGui.QPainter(pixmap)
    text.drawContents(painter, QtCore.QRectF(pixmap.rect()))
    painter.end()

    icon = QtGui.QIcon(pixmap)
    button.setIcon(icon)
    button.setIconSize(pixmap.size())


def show_message_dialog1_(image, opacity=1):
    try:
        dlg = QDialog()
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        dlg.setWindowTitle("報告")
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        dlg_layout = QVBoxLayout()

        wd = QGroupBox()
        wd.setMinimumSize(900, 600)
        set_opacity_on(wd, opacity_value=opacity)
        wd.setStyleSheet(style_sheet.QGroupBoxStyle1(border_radius=10))
        wd_layout = QVBoxLayout()
        top_widget = QtWidgets.QWidget()
        top_layout = QHBoxLayout()

        top_layout.addWidget(lb)
        top_widget.setLayout(top_layout)

        center_widget = QtWidgets.QWidget()
        center_layout = QHBoxLayout()

        lab = QLabel("anh")

        table = QTableWidget()

        center_layout.addWidget(lab)
        center_layout.addWidget(table)
        center_widget.setLayout(center_layout)

        bottom_widget = QtWidgets.QWidget()
        bottom_layout = QHBoxLayout()
        #
        #
        # btn_ok = QDialogButtonBox.Ok
        # dlg.btn_ok = QDialogButtonBox(btn_ok)
        # dlg.btn_ok.setMaximumSize(70, 40)
        # dlg.btn_ok.button(QDialogButtonBox.Ok).setText("OK")
        # dlg.btn_ok.setStyleSheet(style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))
        # set_shadow(dlg.btn_ok)
        # dlg.btn_ok.accepted.connect(dlg.accept)

        btn_close = QDialogButtonBox.Close
        dlg.btn_close = QDialogButtonBox(btn_close)
        dlg.btn_close.setMaximumSize(70, 40)
        dlg.btn_close.button(QDialogButtonBox.Close).setText("閉じる")
        dlg.btn_close.setStyleSheet(style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))
        set_shadow(dlg.btn_close)
        dlg.btn_close.rejected.connect(dlg.close)

        delete = QPushButton()
        delete.setText("xoa")
        bottom_layout.addWidget(dlg.btn_close)
        bottom_layout.addWidget(delete)
        bottom_widget.setLayout(bottom_layout)

        wd_layout.addWidget(top_widget)
        wd_layout.addWidget(center_widget)
        wd_layout.addWidget(bottom_widget)
        wd.setLayout(wd_layout)
        dlg_layout.addWidget(wd)
        dlg.setLayout(dlg_layout)
        resuft = dlg.exec()
        if resuft:
            print("ok")
        else:
            print("k ok")
    except Exception as e:
        print(e)
