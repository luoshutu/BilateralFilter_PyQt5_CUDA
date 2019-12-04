# -*- coding: utf-8 -*-
#Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
#Author             : luoshutu.
#Creat QT Application.

from PyQt5 import QtCore, QtGui

import numpy as np
import time

import bilateralFilter_cu 

class bilateralFilter(object):
    """docstring for bilateralFilter"""
    def __init__(self):
        super(bilateralFilter, self).__init__()
        self.__imageFiltered = np.array
        self.__imageData     = np.array

    def getImageAndFilterParameter(self, inputImage, filModelX, filModelY, s_sigma, r_sigma):
        self.__imageData = self.qimageToNumpy(inputImage)
        self.__imageFiltered = np.zeros([self.__imageData.shape[0], self.__imageData.shape[1]])
        self.__imageFiltered = self.__imageFiltered.astype(np.uint8)

        filterStartTime = time.time()
        self.__filter(filModelX, filModelY, s_sigma, r_sigma)
        filterStopTime  = time.time()
        self.cpuFilterTime = filterStopTime - filterStartTime
        print('FilterTime:', self.cpuFilterTime)

    def getFilteredImage(self):
        outputImage = QtGui.QImage(self.__imageFiltered, self.__imageFiltered.shape[1], 
            self.__imageFiltered.shape[0], QtGui.QImage.Format_Grayscale8) 
        return outputImage, self.cpuFilterTime

    def qimageToNumpy(self, qimage):
        imageTemp = qimage.constBits()
        imageTemp.setsize(qimage.byteCount())
        result = np.array(imageTemp).reshape(qimage.height(), qimage.width())
        print(result.shape)
        return result

    def __filter(self, filModelX, filModelY, s_sigma, r_sigma):
        bilFilKernel = bilateralFilter_cu.bilFilKernel()
        GaussModel = bilFilKernel.creatGaussModel_gpu(filModelX, filModelY, s_sigma)
        print(GaussModel)

        for i in range(self.__imageData.shape[0]):
            for j in range(self.__imageData.shape[1]):
                H = np.zeros([filModelX, filModelY])
                B = np.zeros([filModelX, filModelY])
                F = np.zeros([filModelX, filModelY])
                centralValue = self.__imageData[i, j]
                for m in range(filModelX):
                    for n in range(filModelY):
                        y_index = i + m - int(filModelX / 2)
                        x_index = j + n - int(filModelY / 2)
                        if (y_index >= 0) and (y_index < self.__imageData.shape[0]) and \
                        (x_index >= 0) and (x_index < self.__imageData.shape[1]):
                            currentValue = self.__imageData[y_index, x_index]
                            xx           = (float(currentValue) - float(centralValue)) ** 2
                            H[m, n]      = np.exp(-xx / (2 * (r_sigma ** 2)))
                            F[m, n]      = H[m, n] * GaussModel[m, n]
                            B[m, n]      = F[m, n] * currentValue
                self.__imageFiltered[i, j] = np.sum(B) / np.sum(F)

