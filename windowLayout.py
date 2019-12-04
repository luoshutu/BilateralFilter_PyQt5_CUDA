# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 500)
        MainWindow.setMinimumSize(QtCore.QSize(600, 400))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setMinimumSize(QtCore.QSize(100, 0))
        self.textBrowser.setMaximumSize(QtCore.QSize(100, 16777215))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 3, 2, 1)
        self.labelParameterAdjust = QtWidgets.QLabel(self.centralwidget)
        self.labelParameterAdjust.setObjectName("labelParameterAdjust")
        self.gridLayout.addWidget(self.labelParameterAdjust, 1, 0, 1, 1)
        self.buttonFilter = QtWidgets.QPushButton(self.centralwidget)
        self.buttonFilter.setObjectName("buttonFilter")
        self.gridLayout.addWidget(self.buttonFilter, 1, 2, 1, 1)
        self.layoutImage = QtWidgets.QGridLayout()
        self.layoutImage.setContentsMargins(5, 5, 5, 5)
        self.layoutImage.setHorizontalSpacing(10)
        self.layoutImage.setVerticalSpacing(6)
        self.layoutImage.setObjectName("layoutImage")
        self.labelTitleResult = QtWidgets.QLabel(self.centralwidget)
        self.labelTitleResult.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitleResult.setObjectName("labelTitleResult")
        self.layoutImage.addWidget(self.labelTitleResult, 0, 2, 1, 1)
        self.labelTitleSrc = QtWidgets.QLabel(self.centralwidget)
        self.labelTitleSrc.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitleSrc.setObjectName("labelTitleSrc")
        self.layoutImage.addWidget(self.labelTitleSrc, 0, 1, 1, 1)
        self.labelSrcImage = QtWidgets.QLabel(self.centralwidget)
        self.labelSrcImage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelSrcImage.setText("")
        self.labelSrcImage.setObjectName("labelSrcImage")
        self.layoutImage.addWidget(self.labelSrcImage, 1, 1, 1, 1)
        self.labelResultImage = QtWidgets.QLabel(self.centralwidget)
        self.labelResultImage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelResultImage.setText("")
        self.labelResultImage.setObjectName("labelResultImage")
        self.layoutImage.addWidget(self.labelResultImage, 1, 2, 1, 1)
        self.layoutImage.setRowStretch(1, 1)
        self.gridLayout.addLayout(self.layoutImage, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(891, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 23))
        self.menubar.setObjectName("menubar")
        self.menuSection = QtWidgets.QMenu(self.menubar)
        self.menuSection.setObjectName("menuSection")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoadImage = QtWidgets.QAction(MainWindow)
        self.actionLoadImage.setObjectName("actionLoadImage")
        self.menuSection.addAction(self.actionLoadImage)
        self.menubar.addAction(self.menuSection.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Filter By LuoShutu"))
        self.labelParameterAdjust.setText(_translate("MainWindow", "参数调节："))
        self.buttonFilter.setText(_translate("MainWindow", "滤波"))
        self.labelTitleResult.setText(_translate("MainWindow", "结果图像"))
        self.labelTitleSrc.setText(_translate("MainWindow", "原始图像"))
        self.menuSection.setTitle(_translate("MainWindow", "选择"))
        self.actionLoadImage.setText(_translate("MainWindow", "加载图片"))
