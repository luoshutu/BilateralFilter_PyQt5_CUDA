# -*- coding: utf-8 -*-
#Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
#Author             : luoshutu.
#Creat QT Process Funcation.

import windowLayout as winLay
import bilateralFilter

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

    #初始化UI的一些显示以及功能
    def initUI(self):
        self.ui.textBrowser.append('运行时间：')

    #初始定义一些数据缓存
    def initData(self):
        self.srcImage    = QtGui.QImage()
        self.resultImage = QtGui.QImage()
        self.imagePath   = ''

    #连接信号与槽函数
    def initSlots(self):
        self.ui.actionLoadImage.triggered.connect(self.on_getImage)
        self.ui.buttonFilter.clicked.connect(self.on_bilateralFilter)

    #打开文件路径并获取图像
    def on_getImage(self, QAction):
        self.imagePath, _ = QFileDialog.getOpenFileName(self, 
            'Open Image', '', 'Image files (*.jpg *.gif *.png *.jpeg)')                                 #第二个返回变量为文件类型，可以不使用，但是需占位

        if self.imagePath == '':
            self.ui.textBrowser.append('图像路径为空！')
            return

        self.srcImage = QtGui.QImage(self.imagePath).convertToFormat(QtGui.QImage.Format_Grayscale8)    #以QImage形式获取图像，并转化为8位灰度图像
        #self.srcImage = self.srcImage.scaled(256, 256, QtCore.Qt.KeepAspectRatio)                      #重设图像大小，但该函数不考虑采样优化
        imageMap = QtGui.QPixmap(self.srcImage).scaled(                                                 #将QImage转化为QPixMap形式，方便在label上显示
            self.ui.labelSrcImage.width(), 
            self.ui.labelSrcImage.height(), 
            QtCore.Qt.KeepAspectRatio, 
            QtCore.Qt.SmoothTransformation)
        #print(ImageMap.width())
        self.ui.labelSrcImage.setPixmap(imageMap)
        #self.ui.labelSrcImage.setScaledContents(True)                                                  #设置图像填充满窗口，不考虑比例

    #滤波
    def on_bilateralFilter(self):
        #判断当前是否有输入图像
        if self.imagePath == '':
            self.ui.textBrowser.append('未输入图像！')
            return

        bilFilter = bilateralFilter.bilateralFilter()
        bilFilter.getImageAndFilterParameter(self.srcImage, 15, 15, 4.0, 8.0)                               #传入待滤波的图像、滤波器核大小和方差

        self.resultImage, FilterTime = bilFilter.getFilteredImage()
        FrameNum   = str(int(1 / FilterTime))
        FilterTime = str(round(FilterTime, 6))                                                          #将数值型变量转化为字符串，便于显示，使用round函数保留小数点后6位
        self.ui.textBrowser.append("Filter Time:" + FilterTime + '\n'+ "Frame Num:" + FrameNum)         #在textBrowser中显示滤波花费时间，以及帧数

        imageMap = QtGui.QPixmap(self.resultImage).scaled(
            self.ui.labelResultImage.width(), 
            self.ui.labelResultImage.height(), 
            QtCore.Qt.KeepAspectRatio)
        self.ui.labelResultImage.setPixmap(imageMap)

    #重写窗体size变化时间，用于重新获取图像数据并显示，实现图像大小随窗体大小变化而变化
    def resizeEvent(self, e):
        #获取图像并设置大小
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







