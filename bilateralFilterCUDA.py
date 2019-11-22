# -*- coding: utf-8 -*-
#Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
#Author             : luoshutu.
#Creat QT Application.

from PyQt5 import QtCore, QtGui

import numpy as np

class bilateralFilter(object):
    """docstring for bilateralFilter"""
    def __init__(self):
        super(bilateralFilter, self).__init__()

    def getImageAndFilterParameter(self, inputImage, filModelX, filModelY, s_sigma, r_sigma):
        imageData = self.qimageToNumpy(inputImage)
        self.filter(imageData, filModelX, filModelY, s_sigma, r_sigma)

    def getFilteredImage(self):
        self.outputImage = QtGui.QImage(self.imageData, self.imageData.shape[1], 
            self.imageData.shape[0], QtGui.QImage.Format_Grayscale8) 
        return self.outputImage

    def filter(self, imageData, filModelX, filModelY, s_sigma, r_sigma):
        GaussModel = np.array
        for i in range(filModelX):
            for j in range(filModelY):
                GaussModel[i, j] = 1

    def qimageToNumpy(self, qimage):
        imageTemp = qimage.constBits()
        imageTemp.setsize(qimage.byteCount())

        result = np.array(imageTemp).reshape(qimage.height(), qimage.width())
        print(result.shape)
        return result
