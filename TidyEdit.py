# -*- coding: utf-8 -*-

import sys

import cv2
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
from PyQt5.QtCore import QRect, Qt, QCoreApplication, QMetaObject
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget, QLabel, QComboBox, QPushButton, \
    QApplication, QSlider, QMenuBar, QStatusBar


class UiMainWindow(QMainWindow):

    def __init__(self, main_window):
        super().__init__()

        self.original_image = None
        self.edited_image = None
        self.copy_image = None
        self.is_loaded = False
        self.is_grayscale = False
        self.is_slider = False

        self.x_start, self.y_start, self.x_end, self.y_end = 0, 0, 0, 0
        self.cropping = False
        self.flag = True

        main_window.setObjectName('BBM413 TP')
        main_window.resize(1115, 766)

        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName('central_widget')
        self.source_photo = QLabel(self.central_widget)
        self.central_widget.setStyleSheet('QWidget {background-color: floralwhite}')

        self.source_photo.setGeometry(QRect(8, 360, 551, 371))
        self.source_photo.setText('')
        self.source_photo.setScaledContents(True)
        self.source_photo.setObjectName('source_photo')

        self.label = QLabel(self.central_widget)
        self.label.setGeometry(QRect(568, 360, 541, 371))
        self.label.setText('')
        self.label.setScaledContents(True)
        self.label.setObjectName('label')

        self.filter_combo_box = QComboBox(self.central_widget)
        self.filter_combo_box.setGeometry(QRect(10, 180, 241, 41))
        self.filter_combo_box.setObjectName('filter_combo_box')
        self.filter_combo_box.currentTextChanged.connect(self.filter_menu_sliders)
        self.filter_combo_box.setStyleSheet(
            'QComboBox {background-color: lightcyan;  border-radius: 5px;  font: italic 13px; }')
        self.filter_combo_box.hide()

        self.apply_filter_button = QPushButton(self.central_widget)
        self.apply_filter_button.setGeometry(QRect(500, 180, 121, 41))
        self.apply_filter_button.setObjectName('apply_filter_button')
        self.apply_filter_button.clicked.connect(self.filter_menu_buttons)
        self.apply_filter_button.setStyleSheet(
            'QPushButton {background-color: lightcyan;  border-radius: 5px;  font: 14px; }')
        self.apply_filter_button.hide()

        self.load_image_button = QPushButton(self.central_widget)
        self.load_image_button.setGeometry(QRect(40, 50, 161, 61))
        self.load_image_button.setObjectName('load_image_button')
        self.load_image_button.clicked.connect(self.load_image)
        self.load_image_button.setStyleSheet(
            'QPushButton {background-color: azure; border-style: solid; border-width: 1px; border-radius: 5px; '
            'border-color: aquamarine; font: bold 14px; }')

        self.save_button = QPushButton(self.central_widget)
        self.save_button.setGeometry(QRect(920, 50, 161, 61))
        self.save_button.setObjectName('save_button')
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setStyleSheet(
            'QPushButton {background-color: lavenderblush; border-style: solid; border-width: 1px; border-radius: '
            '5px; border-color: khaki; font: bold 14px; }')
        self.save_button.hide()

        self.reset_button = QPushButton(self.central_widget)
        self.reset_button.setGeometry(QRect(900, 180, 201, 41))
        self.reset_button.setObjectName('reset_button')
        self.reset_button.clicked.connect(self.reset_image)
        self.reset_button.setStyleSheet('QPushButton {background-color: lightcyan;  border-radius: 5px;  font: 14px; }')
        self.reset_button.hide()

        main_window.setCentralWidget(self.central_widget)

        self.menu_bar = QMenuBar(main_window)
        self.menu_bar.setGeometry(QRect(0, 0, 1115, 26))
        self.menu_bar.setObjectName('menu_bar')

        main_window.setMenuBar(self.menu_bar)

        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName('statusbar')

        main_window.setStatusBar(self.statusbar)

        self.slider_angle = QSlider(self.central_widget)
        self.slider_angle.setGeometry(QRect(405, 300, 320, 16))
        self.slider_angle.setOrientation(Qt.Orientation.Horizontal)
        self.slider_angle.setStyleSheet('QSlider::handle:horizontal {background-color: orange; border-radius: 6px;}')
        self.slider_angle.valueChanged.connect(self.rotate_angle)

        self.slider_brightness = QSlider(self.central_widget)
        self.slider_brightness.setGeometry(QRect(405, 300, 320, 16))
        self.slider_brightness.setOrientation(Qt.Orientation.Horizontal)
        self.slider_brightness.setStyleSheet(
            'QSlider::handle:horizontal {background-color: orange; border-radius: 6px;}')
        self.slider_brightness.valueChanged.connect(self.adjust_brightness)

        self.slider_contrast = QSlider(self.central_widget)
        self.slider_contrast.setGeometry(QRect(405, 300, 320, 16))
        self.slider_contrast.setOrientation(Qt.Orientation.Horizontal)
        self.slider_contrast.setStyleSheet('QSlider::handle:horizontal {background-color: orange; border-radius: 6px;}')
        self.slider_contrast.valueChanged.connect(self.adjust_contrast)

        self.slider_saturation = QSlider(self.central_widget)
        self.slider_saturation.setGeometry(QRect(405, 300, 320, 16))
        self.slider_saturation.setOrientation(Qt.Orientation.Horizontal)
        self.slider_contrast.setStyleSheet('QSlider::handle:horizontal {background-color: orange; border-radius: 6px;}')
        self.slider_saturation.valueChanged.connect(self.adjust_saturation)

        self.slider_red = QSlider(self.central_widget)
        self.slider_red.setGeometry(QRect(405, 280, 320, 16))
        self.slider_red.setOrientation(Qt.Orientation.Horizontal)
        self.slider_red.setStyleSheet('QSlider::handle:horizontal {background-color: red; border-radius: 6px;}')
        self.slider_red.valueChanged.connect(self.change_color_balance)

        self.slider_green = QSlider(self.central_widget)
        self.slider_green.setGeometry(QRect(405, 300, 320, 16))
        self.slider_green.setOrientation(Qt.Orientation.Horizontal)
        self.slider_green.setStyleSheet(
            'QSlider::handle:horizontal {background-color: lightgreen; border-radius: 6px;}')
        self.slider_green.valueChanged.connect(self.change_color_balance)

        self.slider_blue = QSlider(self.central_widget)
        self.slider_blue.setGeometry(QRect(405, 320, 320, 16))
        self.slider_blue.setOrientation(Qt.Orientation.Horizontal)
        self.slider_blue.setStyleSheet('QSlider::handle:horizontal {background-color: blue; border-radius: 6px;}')
        self.slider_blue.valueChanged.connect(self.change_color_balance)

        self.slider_noise = QSlider(self.central_widget)
        self.slider_noise.setGeometry(QRect(405, 300, 320, 16))
        self.slider_noise.setOrientation(Qt.Orientation.Horizontal)
        self.slider_noise.setStyleSheet('QSlider::handle:horizontal {background-color: orange; border-radius: 6px;}')
        self.slider_noise.valueChanged.connect(self.add_noise)

        self.error_message = QMessageBox()
        self.error_message.setIcon(QMessageBox.Critical)
        self.error_message.setWindowTitle('ERROR')

        self.ui_window(main_window)

        QMetaObject.connectSlotsByName(main_window)

    def ui_window(self, main_window):

        translated = QCoreApplication.translate
        main_window.setWindowTitle(translated('MainWindow', 'Welcome to Edit-ins'))

        self.apply_filter_button.setText(translated('MainWindow', 'Apply Filter'))
        self.load_image_button.setText(translated('MainWindow', 'Load Image'))
        self.save_button.setText(translated('MainWindow', 'Save'))
        self.reset_button.setText(translated('MainWindow', 'Reset Filters'))

        Filters = ['Blur', 'Deblur', 'Grayscale', 'Crop', 'Flip', 'Mirror', 'Rotate Right', 'Rotate Left',
                   'Rotate Angle', 'Reverse Color', 'Change Color Balance', 'Adjust Brightness', 'Adjust Contrast',
                   'Adjust Saturation', 'Add Noise', 'Detect Edges']

        self.filter_combo_box.addItems(Filters)

    def filter_menu_buttons(self):

        if self.filter_combo_box.currentText() == 'Blur':
            self.blur()
        elif self.filter_combo_box.currentText() == 'Deblur':
            self.de_blur()
        elif self.filter_combo_box.currentText() == 'Grayscale':
            self.grayscale()
        elif self.filter_combo_box.currentText() == 'Crop':
            self.flag_function()
        elif self.filter_combo_box.currentText() == 'Flip':
            self.flip()
        elif self.filter_combo_box.currentText() == 'Mirror':
            self.mirror()
        elif self.filter_combo_box.currentText() == 'Rotate Right':
            self.rotate_right()
        elif self.filter_combo_box.currentText() == 'Rotate Left':
            self.rotate_left()
        elif self.filter_combo_box.currentText() == 'Rotate Angle':
            self.rotate_angle()
        elif self.filter_combo_box.currentText() == 'Reverse Color':
            self.reverse_color()
        elif self.filter_combo_box.currentText() == 'Detect Edges':
            self.detect_edges()

    def filter_menu_sliders(self):
        self.copy_image = self.edited_image

        if self.filter_combo_box.currentText() == 'Adjust Brightness':
            self.is_slider = True

            self.slider_brightness.setValue(49)
            self.slider_brightness.show()

            self.apply_filter_button.hide()

            self.slider_contrast.hide()
            self.slider_saturation.hide()
            self.slider_noise.hide()
            self.slider_angle.hide()

            self.slider_red.hide()
            self.slider_green.hide()
            self.slider_blue.hide()

        elif self.filter_combo_box.currentText() == 'Adjust Contrast':
            self.is_slider = True

            self.slider_contrast.setMaximum(10)
            self.slider_contrast.setMinimum(0)
            self.slider_contrast.setValue(5)
            self.slider_contrast.show()

            self.apply_filter_button.hide()

            self.slider_brightness.hide()
            self.slider_saturation.hide()
            self.slider_angle.hide()
            self.slider_noise.hide()

            self.slider_red.hide()
            self.slider_green.hide()
            self.slider_blue.hide()

        elif self.filter_combo_box.currentText() == 'Adjust Saturation':
            self.is_slider = True

            self.slider_saturation.setValue(49)
            self.slider_saturation.show()

            self.apply_filter_button.hide()

            self.slider_brightness.hide()
            self.slider_contrast.hide()
            self.slider_angle.hide()
            self.slider_noise.hide()

            self.slider_red.hide()
            self.slider_green.hide()
            self.slider_blue.hide()

        elif self.filter_combo_box.currentText() == 'Change Color Balance':
            self.is_slider = True

            self.slider_red.setValue(49)
            self.slider_green.setValue(49)
            self.slider_blue.setValue(49)
            self.slider_red.show()
            self.slider_green.show()
            self.slider_blue.show()

            self.apply_filter_button.hide()

            self.slider_brightness.hide()
            self.slider_contrast.hide()
            self.slider_saturation.hide()
            self.slider_angle.hide()
            self.slider_noise.hide()

        elif self.filter_combo_box.currentText() == 'Add Noise':
            self.is_slider = True

            self.slider_noise.setValue(0)
            self.slider_noise.show()

            self.apply_filter_button.hide()

            self.slider_brightness.hide()
            self.slider_contrast.hide()
            self.slider_saturation.hide()
            self.slider_angle.hide()

            self.slider_red.hide()
            self.slider_green.hide()
            self.slider_blue.hide()

        elif self.filter_combo_box.currentText() == 'Rotate Angle':
            self.is_slider = True

            self.slider_angle.setMaximum(360)
            self.slider_angle.setMinimum(0)
            self.slider_angle.setValue(0)
            self.slider_angle.show()

            self.apply_filter_button.hide()

            self.slider_brightness.hide()
            self.slider_contrast.hide()
            self.slider_saturation.hide()
            self.slider_noise.hide()

            self.slider_red.hide()
            self.slider_green.hide()
            self.slider_blue.hide()

        else:

            if self.is_loaded:
                self.apply_filter_button.show()

            self.is_slider = False

            self.slider_brightness.hide()
            self.slider_contrast.hide()
            self.slider_saturation.hide()
            self.slider_angle.hide()
            self.slider_noise.hide()

            self.slider_red.hide()
            self.slider_green.hide()
            self.slider_blue.hide()

    def load_image(self):

        filename = QFileDialog.getOpenFileName(self, 'Open File', '', 'Images (*.png *.jpg *.jpeg *.tif *tiff)')

        if filename == ('', ''):
            self.error_message.setText('Load Image Error')
            self.error_message.setInformativeText('Please select valid image !')
            self.error_message.exec_()
            return

        image = cv2.cvtColor(cv2.imread(filename[0]), cv2.COLOR_BGR2RGB)

        self.filter_combo_box.show()

        if not self.is_slider:
            self.apply_filter_button.show()

        self.save_button.show()
        self.reset_button.show()

        self.original_image = image
        self.edited_image = image
        self.copy_image = image

        self.is_loaded = True
        self.is_grayscale = False
        self.reset_sliders()

        self.source_photo.setPixmap(QPixmap(filename[0]))
        self.label.setPixmap(QPixmap(filename[0]))

    def save_image(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', 'Edited', 'Images (*.png *.jpg)', )

        if filename == ('', ''):
            self.error_message.setText('Save Image Error')
            self.error_message.setInformativeText('Please select valid path !')
            self.error_message.exec_()
            return

        cv2.imwrite(filename[0], cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2RGB))

    def show_image(self, target_image):

        self.edited_image = target_image

        dimensions = target_image.shape

        if len(dimensions) == 3:
            height, width, channel = dimensions[0], dimensions[1], dimensions[2]
            bytes_per_line = channel * width
            qt_formatted_image = QImage(target_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            height, width = dimensions[0], dimensions[1]
            qt_formatted_image = QImage(target_image.data, width, height, width, QImage.Format_Grayscale8)

        self.label.setPixmap(QPixmap.fromImage(qt_formatted_image))

    def reset_image(self):

        self.copy_image = self.original_image
        self.show_image(self.original_image)
        self.is_grayscale = False

        self.reset_sliders()

    def reset_sliders(self):

        self.slider_angle.setValue(0)
        self.slider_brightness.setValue(49)
        self.slider_contrast.setValue(5)
        self.slider_saturation.setValue(49)
        self.slider_red.setValue(49)
        self.slider_green.setValue(49)
        self.slider_blue.setValue(49)
        self.slider_noise.setValue(0)

    def blur(self):
        pil_image = Image.fromarray(self.edited_image)
        target_image = pil_image.filter(ImageFilter.GaussianBlur(radius=3))
        target_image = np.array(target_image)
        self.show_image(target_image)

    def de_blur(self):
        pil_image = Image.fromarray(self.edited_image)
        enhancer = ImageEnhance.Sharpness(pil_image)
        target_image = enhancer.enhance(3)
        target_image = np.array(target_image)
        self.show_image(target_image)

    def grayscale(self):
        if self.is_grayscale:
            self.error_message.setText('Grayscale Error')
            self.error_message.setInformativeText('Edited image is already grayscale image !')
            self.error_message.exec_()
            return

        target_image = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2GRAY)
        self.is_grayscale = True
        self.show_image(target_image)

    def crop(self, event, x, y, a, b):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x_start, self.y_start, self.x_end, self.y_end = x, y, x, y
            self.cropping = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.cropping:
                self.x_end, self.y_end = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            self.x_end, self.y_end = x, y
            self.cropping = False
            ref_point = [(self.x_start, self.y_start), (self.x_end, self.y_end)]

            if len(ref_point) == 2:
                roi = self.edited_image[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
                if roi.size == 0:
                    self.error_message.setText('Crop Error')
                    self.error_message.setInformativeText('Please click and drag toward the bottom right direction !')
                    self.error_message.exec_()
                    return
                roi = np.array(roi)
                roi = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
                self.show_image(roi)

            self.flag = False

            cv2.destroyAllWindows()

    def flag_function(self):
        self.edited_image = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2RGB)
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.crop)

        while self.flag:
            copied_image = self.edited_image.copy()
            if not self.cropping:
                cv2.imshow('image', self.edited_image)

            elif self.cropping:
                cv2.rectangle(copied_image, (self.x_start, self.y_start), (self.x_end, self.y_end), (255, 0, 0), 2)
                cv2.imshow('image', copied_image)
            cv2.waitKey(1)

        self.flag = True

    def flip(self):
        target_image = cv2.flip(self.edited_image, flipCode=0)
        self.show_image(target_image)

    def mirror(self):
        target_image = cv2.flip(self.edited_image, flipCode=1)
        self.show_image(target_image)

    def rotate_right(self):
        target_image = cv2.rotate(self.edited_image, rotateCode=cv2.ROTATE_90_CLOCKWISE)
        self.show_image(target_image)

    def rotate_left(self):
        target_image = cv2.rotate(self.edited_image, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.show_image(target_image)

    def rotate_angle(self):
        target_image = self.pil_image_generator(1)
        self.show_image(target_image)

    def reverse_color(self):

        pil_image = Image.fromarray(self.edited_image)
        target_image = ImageOps.invert(pil_image)
        target_image = np.array(target_image)
        self.show_image(target_image)

    def change_color_balance(self):

        if self.is_grayscale:
            self.error_message.setText('Color Balance Error')
            self.error_message.setInformativeText(
                'Since the image is grayscale, the color balance settings cannot be changed !')
            self.error_message.exec_()
            return

        target_image = self.pil_image_generator(2)
        self.show_image(target_image)

    def adjust_brightness(self):
        target_image = self.pil_image_generator(3)
        self.show_image(target_image)

    def adjust_contrast(self):
        target_image = self.pil_image_generator(4)
        self.show_image(target_image)

    def adjust_saturation(self):

        if self.is_grayscale:
            self.error_message.setText('Adjust Saturation Error')
            self.error_message.setInformativeText(
                'Since the image is grayscale, the saturation settings cannot be changed !')
            self.error_message.exec_()
            return

        target_image = self.pil_image_generator(5)
        self.show_image(target_image)

    def add_noise(self):
        target_image = self.copy_image.copy()

        if len(target_image.shape) == 2:
            black = 0
            white = 255
        else:
            black = np.array([0, 0, 0], dtype='uint8')
            white = np.array([255, 255, 255], dtype='uint8')

        probabilities = np.random.random(target_image.shape[:2])
        target_image[probabilities < (self.slider_noise.value() * 9 / 1000 / 2)] = black
        target_image[probabilities > 1 - (self.slider_noise.value() * 9 / 1000 / 2)] = white

        self.show_image(target_image)

    def detect_edges(self):
        target_image = cv2.GaussianBlur(self.edited_image, (5, 5), 2)
        target_image = cv2.Canny(target_image, 30, 200)
        self.is_grayscale = True
        self.show_image(target_image)

    def pil_image_generator(self, mode):
        pil_image = Image.fromarray(self.copy_image)

        if mode == 1:
            pil_image = Image.fromarray(self.copy_image)
            im_output = pil_image.rotate(self.slider_angle.value(), expand=True)
        elif mode == 2:
            r, g, b = pil_image.split()

            r = r.point(lambda i: i * self.slider_red.value() / 50)
            g = g.point(lambda j: j * self.slider_green.value() / 50)
            b = b.point(lambda k: k * self.slider_blue.value() / 50)

            im_output = Image.merge('RGB', (r, g, b))
        elif mode == 3:
            enhancer = ImageEnhance.Brightness(pil_image)
            im_output = enhancer.enhance(self.slider_brightness.value() / 50)
        elif mode == 4:
            enhancer = ImageEnhance.Contrast(pil_image)
            im_output = enhancer.enhance(self.slider_contrast.value() / 5)
        elif mode == 5:
            enhancer = ImageEnhance.Color(pil_image)
            im_output = enhancer.enhance(self.slider_saturation.value() / 50)
        else:
            im_output = None

        return np.array(im_output)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = UiMainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
