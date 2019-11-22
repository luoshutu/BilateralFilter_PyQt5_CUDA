# -*- coding: utf-8 -*-
#Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
#Author             : luoshutu.
#Creat QT Process Funcation.

import windowLayout as winLay
import bilateralFilterCUDA

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtGui import QResizeEvent

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = winLay.Ui_MainWindow()
        self.ui.setupUi(self)

        self.initUI()
        self.initData()
        self.initSlots()

        self.show()

    def initUI(self):
        self.ui.textBrowser.append('运行时间：')

    def initData(self):
        self.srcImage    = QtGui.QImage()
        self.resultImage = QtGui.QImage()
        self.imagePath   = ''

    def initSlots(self):
        self.ui.actionLoadImage.triggered.connect(self.on_getImage)
        self.ui.buttonFilter.clicked.connect(self.on_bilateralFilter)

    def on_getImage(self, QAction):
        self.imagePath, _ = QFileDialog.getOpenFileName(self, 
            'Open Image', '', 'Image files (*.jpg *.gif *.png *.jpeg)')

        if self.imagePath == '':
            self.ui.textBrowser.append('图像路径为空！')
            return

        self.srcImage = QtGui.QImage(self.imagePath).convertToFormat(QtGui.QImage.Format_Grayscale8)

        imageMap = QtGui.QPixmap(self.srcImage).scaled(
            self.ui.labelSrcImage.width(), 
            self.ui.labelSrcImage.height(), 
            QtCore.Qt.KeepAspectRatio, 
            QtCore.Qt.SmoothTransformation)

        #print(ImageMap.width())
        self.ui.labelSrcImage.setPixmap(imageMap)
        #self.ui.labelSrcImage.setScaledContents(True)

    def on_bilateralFilter(self):
        if self.imagePath == '':
            self.ui.textBrowser.append('未输入图像！')
            return

        bilFilter = bilateralFilterCUDA.bilateralFilter()
        bilFilter.getImageAndFilterParameter(self.srcImage, 15, 15, 4, 8)

        self.resultImage = bilFilter.getFilteredImage()
        imageMap = QtGui.QPixmap(self.resultImage).scaled(
            self.ui.labelResultImage.width(), 
            self.ui.labelResultImage.height(), 
            QtCore.Qt.KeepAspectRatio)

        self.ui.labelResultImage.setPixmap(imageMap)

    def resizeEvent(self, e):
        imageMap = QtGui.QPixmap(self.srcImage).scaled(
            self.ui.labelSrcImage.width(), 
            self.ui.labelSrcImage.height(), 
            QtCore.Qt.KeepAspectRatio)

        self.ui.labelSrcImage.setPixmap(imageMap)

        imageMap = QtGui.QPixmap(self.resultImage).scaled(
            self.ui.labelResultImage.width(), 
            self.ui.labelResultImage.height(), 
            QtCore.Qt.KeepAspectRatio)

        self.ui.labelResultImage.setPixmap(imageMap)







