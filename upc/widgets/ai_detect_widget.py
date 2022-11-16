import datetime
import threading
import time
from datetime import datetime
import cv2
import json
import numpy as np
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from upc.common import style_sheet, general
from collections import OrderedDict
from upc.common.general import LOGGER


class TableView(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)

        self.create_ui()

    def create_ui(self):
        self.setAlternatingRowColors(True)
        self.setStyleSheet(style_sheet.QTableStyle())


class Images:
    def __init__(self):
        super(Images, self).__init__()
        self.image = None
        self.draw_image = None
        self.detected_count = None
        self.detected_bbox = None
        self.camera = None
        self.descriptions = {'CAMERA': "",
                             'TIME': "",
                             'INDEX': -1}

    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def setDrawImage(self, draw_image):
        self.draw_image = draw_image

    def getDrawImage(self):
        return self.draw_image

    def setDetectedCount(self, data):
        self.detected_count = data

    def getDetectedCount(self):
        return self.detected_count

    def setDetectedBBox(self, bbox):
        self.detected_bbox = bbox

    def getDetectedBBox(self):
        return self.detected_bbox

    def setCamera(self, camera):
        self.camera = camera

    def getCamera(self):
        return self.camera

    def setDescriptions(self, camera="", time_="", index=-1):
        self.descriptions['CAMERA'] = camera
        self.descriptions['TIME'] = time_
        self.descriptions['INDEX'] = index

    def getDescriptions(self):
        return self.descriptions


class DetectedImagesWidget(QGroupBox):
    def __init__(self):
        super(DetectedImagesWidget, self).__init__()
        # general.set_shadow(self)
        self.setStyleSheet(style_sheet.QGroupBoxStyle2())
        self.setStyleSheet("background:white;border-radius:10px")
        main_layout = QHBoxLayout()
        # self.setStyleSheet(style_sheet.QGroupBoxStyle2())

        self.image = QLabel()

        title_widget = QtWidgets.QWidget()
        title_layout = QVBoxLayout()

        self.image_index = QLabel()
        self.image_camera = QLabel()
        self.image_time = QLabel()
        title_layout.addWidget(self.image_index, 0, Qt.AlignLeft)
        title_layout.addWidget(self.image_camera, 0, Qt.AlignLeft)
        title_layout.addWidget(self.image_time, 0, Qt.AlignLeft)
        title_widget.setLayout(title_layout)

        main_layout.addWidget(self.image, 7, Qt.AlignHCenter)
        main_layout.addWidget(title_widget, 3, Qt.AlignLeft)
        # main_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(main_layout)

    def setImage(self, image, size_w):
        try:
            img = cv2.resize(image, (0, 0), fx=size_w / image.shape[1], fy=size_w / image.shape[1])
            img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)

            self.image.setPixmap(pixmap)
        except Exception as e:
            print(e)

    def setImageFromFile(self, path):
        bm = QPixmap(path)
        self.image.setPixmap(bm)

    def setTitle(self, index="", camera="", time_=""):
        self.image_index.setText(f" STT :{index} ")
        self.image_camera.setText(f"CAMERA : {camera}")
        self.image_time.setText(f"TIME : {time_}")


class AiDetectWidget(QtWidgets.QWidget):
    add_item_signal = pyqtSignal(object)
    set_item_signal = pyqtSignal(object, object)
    add_item_table_signal = pyqtSignal(object, object, object)

    def __init__(self):
        super(AiDetectWidget, self).__init__()
        self.btn_get_report = None
        self.rpa_qr = None
        self.lb_yl_id = None
        self.lb_center = None
        self.txt_folder = None
        self.btn_choose = None
        self.table_widget = None
        self.back = None
        self.btn_detect = None
        self.count_total = {}
        self.image = None
        self.list_detected_images_total = None
        self.list_detecting_images = None
        self.list_images = None
        self.my_items = None
        self.list_image_widget = None
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        information_widget = QGroupBox()
        information_widget.setStyleSheet(style_sheet.QGroupBoxHeader())
        information_layout = QHBoxLayout()
        general.set_shadow(information_widget)
        self.lb_center = QLabel()
        self.lb_center.setStyleSheet(style_sheet.QLabelStyle(font_size=25))

        yl_widget = QtWidgets.QWidget()
        yl_layout = QHBoxLayout()
        lb_yl_id = QLabel("担当者CD")
        lb_yl_id.setStyleSheet(style_sheet.QLabelStyle())

        self.lb_yl_id = QLabel()
        self.lb_yl_id.setMinimumSize(300, 50)
        self.lb_yl_id.setStyleSheet(style_sheet.QLabelStyle_1(font_size=25, background_color="white"))
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
        self.lb_yl_name.setStyleSheet(style_sheet.QLabelStyle_1(font_size=25, background_color="white"))
        yl_name_layout.addWidget(lb_yl_name)
        yl_name_layout.addWidget(self.lb_yl_name)
        yl_name_widget.setLayout(yl_name_layout)

        self.rpa_qr = QLabel()
        self.rpa_qr.setStyleSheet(style_sheet.QLabelStyle(font_size=25, text_color="white"))

        information_layout.addWidget(self.lb_center, 4, QtCore.Qt.AlignLeft)
        information_layout.addWidget(yl_widget, 2, Qt.AlignRight)
        information_layout.addWidget(yl_name_widget, 3, Qt.AlignRight)
        information_layout.addWidget(self.rpa_qr, 1, Qt.AlignRight)

        information_widget.setLayout(information_layout)

        center_widget = QtWidgets.QWidget()
        center_layout = QHBoxLayout()

        # region Table Widget
        self.table_widget = TableView()
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table_widget.setColumnCount(3)
        self.table_widget.setRowCount(0)
        new_item = QTableWidgetItem("0")
        new_item.setTextAlignment(Qt.AlignHCenter)
        self.table_widget.setItem(3, 0, new_item)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        self.table_widget.setHorizontalHeaderLabels(["商品CD", "商品名", "数"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_widget.setShowGrid(False)
        self.table_widget.setMinimumHeight(600)
        self.table_widget.setStyleSheet(style_sheet.QTableStyle())
        # general.set_shadow(self.table_widget)
        self.add_item_table_signal.connect(self.table_widget.setItem)
        # endregion
        # region List Image Widget
        self.list_image_widget = QListWidget()
        # general.set_shadow(self.list_image_widget)
        self.list_image_widget.setStyleSheet(style_sheet.QListStyle2())
        self.list_image_widget.setFocusPolicy(Qt.NoFocus)
        self.list_image_widget.setMinimumHeight(600)
        self.list_images = []
        self.my_items = []
        self.add_item_signal.connect(self.list_image_widget.addItem)
        self.set_item_signal.connect(self.list_image_widget.setItemWidget)
        self.list_image_widget.itemClicked.connect(self.on_item_image_clicked)
        # endregion

        center_layout.addWidget(self.table_widget, 6, Qt.AlignTop)
        center_layout.addWidget(self.list_image_widget, 4, Qt.AlignTop)
        center_widget.setLayout(center_layout)

        bottom_widget = QtWidgets.QWidget()
        bottom_layout = QHBoxLayout()

        self.back = QToolButton()
        general.set_shadow(self.back)
        self.back.setText("戻る")

        self.back.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15, width=150, height=50, ))

        self.btn_detect = QToolButton()
        general.set_shadow(self.btn_detect)
        self.btn_detect.setText("認識")
        self.btn_detect.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15, width=150, height=50, ))

        self.btn_print = QToolButton()
        general.set_shadow(self.btn_print)
        self.btn_print.setText("確定")
        self.btn_print.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15, width=150, height=50, ))

        self.txt_folder = QLineEdit()
        self.txt_folder.setText("//192.168.0.241/nam/yakult_project/images_processed/check_data")
        self.txt_folder.setStyleSheet(style_sheet.QLineEditStyle())

        self.btn_choose = QToolButton()
        self.btn_choose.setText("選択")
        self.btn_choose.setStyleSheet(style_sheet.QToolButtonStyle(width=150, height=50, padding_top=0))
        self.btn_choose.clicked.connect(self.choose_folder_dialog)

        self.btn_get_report = QToolButton()
        self.btn_get_report.setText("レポート")
        self.btn_get_report.setStyleSheet(style_sheet.QToolButtonStyle(width=150, height=50, padding_top=0))

        self.btn_open_excel = QToolButton()
        self.btn_open_excel.setText("EXCELを開く")
        self.btn_open_excel.setStyleSheet(style_sheet.QToolButtonStyle(width=150, height=50, padding_top=0))

        bottom_layout.addWidget(self.back)
        bottom_layout.addWidget(self.btn_detect)
        bottom_layout.addWidget(self.btn_print)
        bottom_layout.addWidget(self.txt_folder)
        bottom_layout.addWidget(self.btn_choose)
        bottom_layout.addWidget(self.btn_get_report)
        bottom_layout.addWidget(self.btn_open_excel)

        bottom_widget.setLayout(bottom_layout)

        find_widget = QtWidgets.QWidget()

        setting_layout = QHBoxLayout()
        self.cb_create_annotation = QCheckBox("Create Annotation")
        self.cb_create_annotation.setStyleSheet(style_sheet.QCheckBoxStyle())

        self.cb_not_show_conf = QCheckBox("Don't show Confidence")
        self.cb_not_show_conf.setStyleSheet(style_sheet.QCheckBoxStyle())

        self.cb_draw_point = QCheckBox("Draw Point")
        self.cb_draw_point.setStyleSheet(style_sheet.QCheckBoxStyle())
        self.txt_find = QLineEdit()
        self.txt_find.setStyleSheet(style_sheet.QLineEditStyle(width=300))
        self.btn_find = QToolButton()
        self.btn_find.setText("検査")
        self.btn_find.setStyleSheet(style_sheet.QToolButtonStyle(width=150, height=50, margin_top=0,padding_top=0))
        self.btn_find.clicked.connect(self.find_image)
        setting_layout.addWidget(self.cb_create_annotation)
        setting_layout.addWidget(self.cb_draw_point)
        setting_layout.addWidget(self.cb_not_show_conf)
        setting_layout.addWidget(self.txt_find)
        setting_layout.addWidget(self.btn_find)
        find_widget.setLayout(setting_layout)

        main_layout.addWidget(information_widget, 1, Qt.AlignTop)
        main_layout.addWidget(center_widget, 7, Qt.AlignVCenter)
        main_layout.addWidget(find_widget, 1, Qt.AlignRight)
        main_layout.addWidget(bottom_widget, 1, Qt.AlignVCenter)

        self.list_detected_images_total = []
        self.list_detecting_images = []

        self.setLayout(main_layout)

    def clear_layout(self):
        self.table_widget.clear()
        self.table_widget.setColumnCount(3)
        self.table_widget.setRowCount(0)
        new_item = QTableWidgetItem("0")
        new_item.setTextAlignment(Qt.AlignHCenter)
        self.table_widget.setItem(3, 0, new_item)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        self.table_widget.setHorizontalHeaderLabels(["商品CD", "商品名", "数"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_widget.setShowGrid(False)
        self.table_widget.update()
        # self.table_widget.setRowCount(0)
        # self.table_widget.setColumnCount(3)
        # self.table_widget.setHorizontalHeaderLabels(["商品CD", "商品名", "数"])
        self.list_image_widget.clear()
        self.list_detected_images_total = []
        self.list_detecting_images = []
        self.count_total = {}

    def on_cb_checked(self, state):
        if state == Qt.Checked:
            if self.sender() == self.cb_draw_point:
                self.cb_draw_point.setChecked(True)
            if self.sender() == self.cb_create_annotation:
                self.cb_create_annotation.setChecked(True)
            if self.sender()==self.cb_show_conf:
                self.cb_show_conf.setChecked(True)

    def choose_folder_dialog(self):
        file = QFileDialog.getExistingDirectory(self, "フォルダ選択", r"//192.168.0.241/nam/yakult_project/images_processed/check_data")
        self.txt_folder.setText(file)

    def find_image(self):
        if len(self.txt_find.text()) > 0:
            idx = 0
            is_exist = False
            for index, image in enumerate(self.list_detected_images_total):
                print(image.getDescriptions()["CAMERA"].split(" ")[0])
                if image.getDescriptions()["CAMERA"].split(" ")[0] == self.txt_find.text():
                    idx = index
                    is_exist = True
                    break

            if is_exist:
                try:
                    # .list_detected_images_total[index]
                    dlg = ImagesDetailsWidget(self, self.list_detected_images_total[idx], idx)
                    result = dlg.exec()
                    if result:
                        LOGGER.info("OK")
                    else:
                        LOGGER.info("CANCEL")
                except Exception as e:
                    LOGGER.error(e)
            else:
                return

    def update_table_view(self):

        # Count all
        list_cls = []
        list_count = []
        sorted_dic = OrderedDict(sorted(self.count_total.items()))

        list_cls.extend(sorted_dic.keys())
        list_count.extend(sorted_dic.values())

        products_name = []
        products_name_cls = []

        # with open("./assets/classes_name.txt", "r", encoding="UTF-8") as f:
        #     for line in f:
        #         products_name.append(line.strip())
        # for cls in list_cls:
        #     products_name_cls.append(products_name[int(cls)])

        data = {"商品ID": [str(cls.split("_")[0]) for cls in list_cls], "商品名": [cls.split("_")[1] for cls in list_cls],
                "数": [cnt for cnt in list_count], }
        hori_header = []
        cols = (len(data.keys()))
        rows = 0
        for x, y in data.items():
            rows = len(y)
            break

        self.table_widget.setColumnCount(cols)
        self.table_widget.setRowCount(rows)
        for n, key in enumerate(data.keys()):
            hori_header.append(key)
            for m, cnt in enumerate(data[key]):
                new_item = QTableWidgetItem(str(cnt))
                new_item.setTextAlignment(Qt.AlignHCenter)
                self.add_item_table_signal.emit(m, n, new_item)
                self.table_widget.resizeColumnsToContents()
                self.table_widget.viewport().update()
        self.table_widget.resizeRowsToContents()
        self.table_widget.setHorizontalHeaderLabels(hori_header)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_widget.setShowGrid(False)

        LOGGER.info("TABLE UPDATED")

    def update_list_image(self, list_image=None):
        if list_image is not None:
            if list_image is not None:
                for image in list_image:
                    im = DetectedImagesWidget()
                    im.setImage(image.getDrawImage(), 300)
                    im.setTitle(index=image.getDescriptions()['INDEX'],
                                camera=image.getDescriptions()['CAMERA'],
                                time_=image.getDescriptions()['TIME'])
                    my_item = QListWidgetItem()
                    my_item.setSizeHint(im.sizeHint())

                    self.my_items.append(my_item)
                    self.add_item_signal.emit(my_item)
                    self.set_item_signal.emit(my_item, im)
                    self.list_image_widget.update()
            LOGGER.info("LIST IMAGE UPDATED")
            pass
        else:
            if self.list_detecting_images is not None:
                for image in self.list_detecting_images:
                    im = DetectedImagesWidget()
                    im.setImage(image.getDrawImage(), 300)
                    im.setTitle(index=image.getDescriptions()['INDEX'],
                                camera=image.getDescriptions()['CAMERA'],
                                time_=image.getDescriptions()['TIME'])
                    my_item = QListWidgetItem()
                    my_item.setSizeHint(im.sizeHint())

                    self.my_items.append(my_item)
                    self.add_item_signal.emit(my_item)
                    self.set_item_signal.emit(my_item, im)
                    self.list_image_widget.update()
            LOGGER.info("LIST IMAGE UPDATED")

    def on_item_image_clicked(self):
        index = self.list_image_widget.currentRow()
        LOGGER.info(f"ITEM IMAGE AT {index} CLICKED")
        try:
            # .list_detected_images_total[index]
            dlg = ImagesDetailsWidget(self, self.list_detected_images_total[index], index)
            result = dlg.exec()
            if result:
                LOGGER.info("OK")
            else:
                LOGGER.info("CANCEL")
        except Exception as e:
            LOGGER.error(e)

    def get_images(self, camera_loaded, setting):
        t1 = threading.Thread(target=self.open_camera_event,
                              args=[int(camera_loaded["TOP"]), "TOP", int(setting.getTopFocus())])
        t2 = threading.Thread(target=self.open_camera_event,
                              args=[int(camera_loaded["SIDE"]), "SIDE", int(setting.getSideFocus())])
        t1.start()
        t2.start()

    def open_camera_event(self, camera_source, camera, focus):
        cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
        idx = 0
        while True:
            r, frame = cap.read()
            if not r:
                cap.release()
                break
            cap.set(cv2.CAP_PROP_FOCUS, focus)
            if idx == 5:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Images()
                image.setImage(frame.copy())
                image.setDrawImage(frame.copy())
                image.setCamera(camera)
                self.list_detecting_images.append(image)
                # clear memory
                cap.release()
                break
            idx += 1

    def update_list(self, old_cls, old_name, new_cls, new_name, image, box, table, dlg_frame, index_of_list):

        # Update count_total
        old = f"{old_cls}_{old_name}"
        new = f"{new_cls}_{new_name}"
        for cls_name in self.count_total.keys():
            if cls_name == old:
                if int(self.count_total[cls_name]) > 1:
                    self.count_total[cls_name] -= 1
                elif int(self.count_total[cls_name]) == 1:
                    del self.count_total[cls_name]
                break
        if new not in self.count_total.keys():
            self.count_total[new] = 1
        else:
            self.count_total[new] += 1

        # Update image object
        for cls_name in image.getDetectedCount().keys():
            if cls_name == old:
                if int(image.getDetectedCount()[cls_name]) > 1:
                    image.getDetectedCount()[cls_name] -= 1
                elif int(image.getDetectedCount()[cls_name]) == 1:
                    del image.getDetectedCount()[cls_name]
                break
        if new not in image.getDetectedCount().keys():
            image.getDetectedCount()[new] = 1
        else:
            image.getDetectedCount()[new] += 1

        image.getDetectedBBox().remove(box)
        new_box = (box[0], box[1], box[2], box[3], 1, int(new_cls), str(new_name))
        image.getDetectedBBox().append(new_box)
        new_draw_image = image.getImage().copy()
        for box in image.getDetectedBBox():
            (case_x_min, case_y_min, case_x_max, case_y_max, case_conf, case_cls) = (
                int(box[0]), int(box[1]), int(box[2]), int(box[3]), float(box[4]), int(box[5]))

            new_draw_image = self.draw_put_text(new_draw_image, case_x_min, case_y_min, case_x_max,
                                                case_y_max, case_conf, case_cls, point=False)
        image.setDrawImage(new_draw_image)

        self.update_list_on_ai_widget()
        self.update_list_on_details_widget(table, image)
        self.update_image_on_details_widget(dlg_frame, image)
        self.update_image_on_ai_widget()

    @staticmethod
    def update_image_on_details_widget(dlg_frame, image):
        img = cv2.resize(image.getDrawImage(), (0, 0), fx=960 / image.getImage().shape[1],
                         fy=960 / image.getDrawImage().shape[1])
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        dlg_frame.setPixmap(pixmap)

    def update_image_on_ai_widget(self, ):
        # print(self.list_image_widget.item(index))
        # im = DetectedImagesWidget()
        # im.setImage(image.getDrawImage(), 300)
        # im.setTitle(index=image.getDescriptions()['INDEX'],
        #             camera=image.getDescriptions()['CAMERA'],
        #             time_=image.getDescriptions()['TIME'])
        # my_item = QListWidgetItem()
        # my_item.setSizeHint(im.sizeHint())
        #
        # self.my_items.append(my_item)
        # self.add_item_signal.emit(my_item)
        # self.set_item_signal.emit(my_item, im)
        # self.list_image_widget.update()
        # self.list_image_widget.item(index).setDrawImage(draw)
        self.list_image_widget.clear()

        if self.list_detected_images_total is not None:
            for image in self.list_detected_images_total:
                im = DetectedImagesWidget()
                im.setImage(image.getDrawImage(), 300)
                im.setTitle(index=image.getDescriptions()['INDEX'],
                            camera=image.getDescriptions()['CAMERA'],
                            time_=image.getDescriptions()['TIME'])
                my_item = QListWidgetItem()
                my_item.setSizeHint(im.sizeHint())

                self.my_items.append(my_item)
                self.add_item_signal.emit(my_item)
                self.set_item_signal.emit(my_item, im)
                self.list_image_widget.update()

    def update_list_on_ai_widget(self):
        self.update_table_view()

    @staticmethod
    def draw_put_text(draw_img, x1, y1, x2, y2, conf, cls, point=False,show_conf=True):

        if int(conf * 100) >= 80:
            color = (0, 0, 255)  # BLUE
        elif int(conf * 100) >= 50:
            color = (0, 255, 0)  # GREEN
        else:
            color = (255, 0, 0)  # RED
        if point:
            over = draw_img.copy()
            cv2.circle(over, (int(x1 + (x2 - x1) / 2), int(y1 + (y2 - y1) / 2)), 28, color, thickness=-1,
                       lineType=cv2.LINE_4, shift=0)
            alpha = 0.4

            draw_img = cv2.addWeighted(over, alpha, draw_img, 1 - alpha, 0)
            cv2.circle(draw_img, (int(x1 + (x2 - x1) / 2), int(y1 + (y2 - y1) / 2)), 30, color, thickness=5,
                       lineType=cv2.LINE_4,
                       shift=0)
            cv2.putText(draw_img, f"{cls} {int(conf * 100)}%",
                        (int(x1 + (x2 - x1) / 2) - 20, int(y1 + (y2 - y1) / 2) + 10),
                        cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 255, 255), 6, cv2.LINE_AA)
            cv2.putText(draw_img, f"{cls} {int(conf * 100)}%",
                        (int(x1 + (x2 - x1) / 2) - 20, int(y1 + (y2 - y1) / 2) + 10),
                        cv2.FONT_HERSHEY_COMPLEX, 1, color,
                        2, cv2.LINE_AA)
        else:
            # cv2.rectangle(draw_img, (x1, y1),
            #               (x2, y2), color, 2)
            # cv2.putText(draw_img, f"{cls} {int(conf * 100)}%", (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
            #             (255, 255, 255), 6, cv2.LINE_AA)
            # cv2.putText(draw_img, f"{cls} {int(conf * 100)}%", (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_COMPLEX, 1, color,
            #             3, cv2.LINE_AA)
            #

            z = 30
            x = 10
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            if (x2 - x1) < (y2 - y1):
                z = (cx - x1) // 2
                x = z // 3
            else:
                z = (cy - y1) // 2
                x = z // 3

            thickness = 3
            if show_conf:
                text = f"{cls} {int(conf * 100)}%"
            else:
                text = f"{cls}"
            if cls >= 10:
                text_pos = (int(cx - z // 2), int(cy + z // 2))
            else:
                text_pos = (int(cx - z // 3), int(cy + z // 3))

            cv2.putText(draw_img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 5, cv2.LINE_AA)
            cv2.putText(draw_img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        3, cv2.LINE_AA)
            color = (0, 255, 0)
            pts1 = np.array([[cx - z, cy - z + x], [cx - z, cy - z], [cx - z + x, cy - z]], np.int32)
            pts1 = pts1.reshape((-1, 1, 2))
            draw_img = cv2.polylines(draw_img, pts=[pts1], isClosed=False, color=color, thickness=thickness)

            pts1 = np.array([[cx + z, cy - z + x], [cx + z, cy - z], [cx + z - x, cy - z]], np.int32)
            pts1 = pts1.reshape((-1, 1, 2))
            draw_img = cv2.polylines(draw_img, pts=[pts1], isClosed=False, color=color, thickness=thickness)

            pts1 = np.array([[cx - z, cy + z - x], [cx - z, cy + z], [cx - z + x, cy + z]], np.int32)
            pts1 = pts1.reshape((-1, 1, 2))
            draw_img = cv2.polylines(draw_img, pts=[pts1], isClosed=False, color=color, thickness=thickness)

            pts1 = np.array([[cx + z, cy + z - x], [cx + z, cy + z], [cx + z - x, cy + z]], np.int32)
            pts1 = pts1.reshape((-1, 1, 2))
            draw_img = cv2.polylines(draw_img, pts=[pts1], isClosed=False, color=color, thickness=thickness)

        return draw_img

    @staticmethod
    def update_list_on_details_widget(table, image):
        list_cls = []
        list_count = []
        sorted_dic = OrderedDict(sorted(image.getDetectedCount().items()))

        list_cls.extend(sorted_dic.keys())
        list_count.extend(sorted_dic.values())

        products_name = []
        products_name_cls = []

        data = {"商品ID": [str(cls.split("_")[0]) for cls in list_cls], "商品名": [cls.split("_")[1] for cls in list_cls],
                "数": [cnt for cnt in list_count], }
        hori_header = []
        cols = (len(data.keys()))
        rows = 0
        for x, y in data.items():
            rows = len(y)
            break

        table.setColumnCount(cols)
        table.setRowCount(rows)
        for n, key in enumerate(data.keys()):
            hori_header.append(key)
            for m, cnt in enumerate(data[key]):
                new_item = QTableWidgetItem(str(cnt))
                new_item.setTextAlignment(Qt.AlignHCenter)
                table.setItem(m, n, new_item)
                table.resizeColumnsToContents()
                table.viewport().update()
        table.resizeRowsToContents()
        table.setHorizontalHeaderLabels(hori_header)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setShowGrid(False)


class ImagesDetailsWidget(QDialog):
    def __init__(self, parent, image, index):
        super(ImagesDetailsWidget, self).__init__(parent=parent)
        self.y = None
        self.x = None
        self.image = image
        self.paren = parent
        self.index = index

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        dlg_layout = QVBoxLayout()

        wd = QGroupBox()
        # wd.setMinimumSize(900, 600)
        wd.setStyleSheet(style_sheet.QGroupBoxStyle2(border_radius=10, border_width=4))
        wd_layout = QVBoxLayout()
        information_widget = QGroupBox()
        information_widget.setStyleSheet(style_sheet.QGroupBoxStyle2(background_color=style_sheet.main_color))
        information_layout = QHBoxLayout()
        lb_camera = QLabel(self.image.getDescriptions()["CAMERA"])
        lb_camera.setStyleSheet(style_sheet.QLabelStyle(text_color="white"))
        lb_stt = QLabel(str(self.image.getDescriptions()["INDEX"]))
        lb_stt.setStyleSheet(style_sheet.QLabelStyle(text_color="white"))
        lb_time = QLabel(str(self.image.getDescriptions()["TIME"]))
        lb_time.setStyleSheet(style_sheet.QLabelStyle(text_color="white"))

        information_layout.addWidget(lb_camera)
        information_layout.addWidget(lb_stt)
        information_layout.addWidget(lb_time)

        information_widget.setLayout(information_layout)

        center_widget = QtWidgets.QWidget()
        center_layout = QHBoxLayout()

        self.dlg_frame = QLabel()
        self.dlg_frame.setPixmap(general.get_pixmap(960, self.image))
        self.dlg_frame.mousePressEvent = self.get_pos

        self.table_detail = TableView()
        self.table_detail.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_detail.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_detail.setMinimumSize(700, 400)
        list_cls = []
        list_count = []
        sorted_dic = OrderedDict(sorted(image.getDetectedCount().items()))
        list_cls.extend(sorted_dic.keys())
        list_count.extend(sorted_dic.values())

        products_name = []
        products_name_cls = []
        #
        # with open("./assets/classes_name.txt", "r", encoding="UTF-8") as f:
        #     for line in f:
        #         products_name.append(line.strip())
        #
        # for cls in list_cls:
        #     products_name_cls.append(products_name[int(cls)])

        data = {"商品ID": [str(cls.split("_")[0]) for cls in list_cls], "商品名": [cls.split("_")[1] for cls in list_cls],
                "数": [cnt for cnt in list_count], }
        hori_header = []
        cols = (len(data.keys()))
        rows = 0
        for x, y in data.items():
            rows = len(y)
            break

        self.table_detail.setColumnCount(cols)
        self.table_detail.setRowCount(rows)
        for n, key in enumerate(data.keys()):
            hori_header.append(key)
            for m, cnt in enumerate(data[key]):
                new_item = QTableWidgetItem(str(cnt))
                new_item.setTextAlignment(Qt.AlignHCenter)
                self.table_detail.setItem(m, n, new_item)
                self.table_detail.resizeColumnsToContents()
                self.table_detail.viewport().update()
        self.table_detail.resizeRowsToContents()
        self.table_detail.setHorizontalHeaderLabels(hori_header)
        self.table_detail.horizontalHeader().setStretchLastSection(True)
        self.table_detail.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_detail.setShowGrid(False)

        center_layout.addWidget(self.dlg_frame)
        center_layout.addWidget(self.table_detail)
        center_widget.setLayout(center_layout)

        bottom_widget = QtWidgets.QWidget()
        bottom_layout = QHBoxLayout()

        btn_close = QDialogButtonBox.Close
        self.btn_close = QDialogButtonBox(btn_close)
        general.set_shadow(self.btn_close)
        self.btn_close.button(QDialogButtonBox.Close).setText("閉じる")
        self.btn_close.setStyleSheet(
            style_sheet.QPushButtonStyle(height=60, width=100, font_size=20, border_radius=5))
        self.btn_close.rejected.connect(self.close)

        delete = QPushButton()
        general.set_shadow(delete)
        delete.setStyleSheet(style_sheet.QPushButtonStyle(height=60, width=100, font_size=20, border_radius=5, ))
        delete.setText("削除")
        bottom_layout.addWidget(self.btn_close)
        bottom_layout.addWidget(delete)
        bottom_widget.setLayout(bottom_layout)

        wd_layout.addWidget(information_widget)
        wd_layout.addWidget(center_widget)
        wd_layout.addWidget(bottom_widget)
        wd.setLayout(wd_layout)
        dlg_layout.addWidget(wd)
        self.setLayout(dlg_layout)

    def get_pos(self, event):
        images_box = {}

        if event.type() == QEvent.MouseButtonDblClick:
            print("DBClick")
            self.x = event.pos().x()
            self.y = event.pos().y()
            print(f"{self.x} {self.y}")
            # To % format
            x = float(self.x / self.dlg_frame.width())
            y = float(self.y / self.dlg_frame.height())
            print(f"{x} {y}")
            for box in self.image.getDetectedBBox():
                (x1, y1, x2, y2, conf, cls, name) = (
                    int(box[0]), int(box[1]), int(box[2]), int(box[3]), float(box[4]), int(box[5]), str(box[6]))
                img_x1 = float(x1 / self.image.getImage().shape[1])
                img_x2 = float(x2 / self.image.getImage().shape[1])

                img_y1 = float(y1 / self.image.getImage().shape[0])
                img_y2 = float(y2 / self.image.getImage().shape[0])

                if img_x1 < x < img_x2 and img_y1 < y < img_y2:
                    images_box["cls"] = (x1, y1, x2, y2)
                    try:
                        dlg_item_edit = ItemEditWidget(box, self.image, x, y)
                        r = dlg_item_edit.exec()
                        if r:

                            new_cls = dlg_item_edit.line_edit.text().split(":")[0]
                            new_name = dlg_item_edit.line_edit.text().split(":")[1]
                            print(new_cls)
                            self.paren.update_list(cls, name, new_cls, new_name, self.image, box, self.table_detail,
                                                   self.dlg_frame,
                                                   self.index)
                            print("edit ok")
                        else:
                            print("edit khong ok")
                    except Exception as e:
                        print(e)
                    break

        # else:
        #     print("Click")
        #
        #     self.x = event.pos().x()
        #     self.y = event.pos().y()
        #     print(f"{self.x} {self.y}")1`

    def delete_item(self):
        pass


class ItemEditWidget(QDialog):
    def __init__(self, box, image, x, y):
        super(ItemEditWidget, self).__init__()
        self.image = image
        self.bbox = box

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        dlg_layout = QVBoxLayout()

        wd = QGroupBox()
        # wd.setMinimumSize(900, 600)
        wd.setStyleSheet(style_sheet.QGroupBoxStyle2(border_radius=10, border_width=0))
        wd_layout = QVBoxLayout()
        information_widget = QGroupBox()
        information_widget.setStyleSheet(style_sheet.QGroupBoxStyle2())
        information_layout = QHBoxLayout()
        lb_camera = QLabel(self.image.getDescriptions()["CAMERA"])
        lb_camera.setStyleSheet(style_sheet.QLabelStyle())
        lb_stt = QLabel(str(self.image.getDescriptions()["INDEX"]))
        lb_stt.setStyleSheet(style_sheet.QLabelStyle())
        lb_time = QLabel(str(self.image.getDescriptions()["TIME"]))
        lb_time.setStyleSheet(style_sheet.QLabelStyle())

        information_layout.addWidget(lb_camera)
        information_layout.addWidget(lb_stt)
        information_layout.addWidget(lb_time)

        information_widget.setLayout(information_layout)

        center_widget = QtWidgets.QWidget()
        center_layout = QHBoxLayout()

        item_img = QLabel()

        (x1, y1, x2, y2, conf, cls) = (
            int(box[0]), int(box[1]), int(box[2]), int(box[3]), float(box[4]), int(box[5]))
        print("%s %s %s %s " % (x1, x2, y1, y2))
        item_clicked = self.image.getImage()[y1:y2, x1:x2]
        img = cv2.resize(item_clicked, (0, 0), fx=1, fy=1)
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        item_img.setPixmap(pixmap)

        self.line_edit = QLineEdit()
        general.set_shadow(self.line_edit)
        self.line_edit.setMinimumSize(300, 30)
        self.line_edit.adjustSize()
        # reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        # input_validator = QRegExpValidator(reg_ex, self.self.line_edit)
        # self.self.line_edit.setValidator(input_validator)
        self.line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit.setStyleSheet(style_sheet.QLineEditStyle())
        data_load = []

        if self.image.getCamera() == "TOP":

            with open("./assets/top.txt", "r", encoding="UTF-8") as f:
                for line in f:
                    data_load.append(line.strip())
        elif self.image.getCamera() == "SIDE":

            with open("./assets/side.txt", "r", encoding="UTF-8") as f:
                for line in f:
                    data_load.append(line.strip())

        codes = [f"{id_}:{name_}" for id_, name_ in enumerate(data_load)]

        # completer = QCompleter(codes)
        model = QStringListModel()
        model.setStringList(codes)
        completer = QCompleter()
        completer.setModel(model)

        completer.popup().setStyleSheet("font-size:18px;")
        completer.activated.connect(self.on_completer_selected)
        self.line_edit.setCompleter(completer)

        center_layout.addWidget(item_img)
        center_layout.addWidget(self.line_edit, 0, Qt.AlignTop)
        center_widget.setLayout(center_layout)

        bottom_widget = QtWidgets.QWidget()
        bottom_layout = QHBoxLayout()

        btn_ok = QDialogButtonBox.Ok
        self.btn_ok = QDialogButtonBox(btn_ok)
        self.btn_ok.button(QDialogButtonBox.Ok).setText("OK")
        self.btn_ok.setStyleSheet(style_sheet.QPushButtonStyle(height=60, width=100, font_size=20, border_radius=5))
        general.set_shadow(self.btn_ok)
        self.btn_ok.accepted.connect(self.accept)

        btn_close = QDialogButtonBox.Close
        self.btn_close = QDialogButtonBox(btn_close)
        general.set_shadow(self.btn_close)
        self.btn_close.button(QDialogButtonBox.Close).setText("閉じる")
        self.btn_close.setStyleSheet(
            style_sheet.QPushButtonStyle(height=60, width=100, font_size=20, border_radius=5))
        self.btn_close.rejected.connect(self.close)

        bottom_layout.addWidget(self.btn_close)
        bottom_layout.addWidget(self.btn_ok)
        bottom_widget.setLayout(bottom_layout)

        wd_layout.addWidget(information_widget, 0, Qt.AlignTop)
        wd_layout.addWidget(center_widget)
        wd_layout.addWidget(bottom_widget)
        wd.setLayout(wd_layout)
        dlg_layout.addWidget(wd)
        self.setLayout(dlg_layout)

    def on_completer_selected(self):
        product_code = self.line_edit.text().split("：")[0]
        print(product_code)
        # product_type = None
        # for cd in self.data:
        #     if cd["product_code"] == product_code:
        #         self.txt_classification.setText(cd["product_classification"])
        #         self.txt_product_name1.setText(cd["finnish_date"])
        #         if cd["cnt_product_single"] == "1":
        #             self.product_type = "バラ"
        #         if cd["cnt_product_pack"] == "1":
        #             self.product_type = "パーク"
        #         if cd["cnt_product_case"] == "1":
        #             self.product_type = "ケース"
        #         self.txt_product_name2.setText(self.product_type)
        #         self.txt_product_name3.setText(cd["cnt_product_single"])
        #         break
