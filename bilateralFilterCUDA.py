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
        self.__imageFiltered = np.array
        self.__imageData     = np.array
        self.__GaussModel    = np.array

    def getImageAndFilterParameter(self, inputImage, filModelX, filModelY, s_sigma, r_sigma):
        self.__imageData = self.qimageToNumpy(inputImage)
        self.__imageFiltered = np.zeros([self.__imageData.shape[0], self.__imageData.shape[1]])
        self.__filter(filModelX, filModelY, s_sigma, r_sigma)

    def getFilteredImage(self):
        outputImage = QtGui.QImage(self.__imageFiltered, self.__imageFiltered.shape[1], 
            self.__imageFiltered.shape[0], QtGui.QImage.Format_Grayscale8) 
        return outputImage

    def qimageToNumpy(self, qimage):
        imageTemp = qimage.constBits()
        imageTemp.setsize(qimage.byteCount())
        result = np.array(imageTemp).reshape(qimage.height(), qimage.width())
        print(result.shape)
        return result

    def __filter(self, filModelX, filModelY, s_sigma, r_sigma):
        self.__creatGaussModel(filModelX, filModelY, s_sigma)
        for i in range(self.__imageData.shape[0]):
            for j in range(self.__imageData.shape[1]):
                H = np.zeros([filModelX, filModelY])
                B = np.zeros([filModelX, filModelY])
                F = np.zeros([filModelX, filModelY])
                centralValue = self.__imageData[i, j]
                for m in range(filModelX):
                    for n in range(filModelY):
                        y_index = i + m - 6
                        x_index = j + n - 6
                        if (y_index >= 0) and (y_index < self.__imageData.shape[0]) and \
                        (x_index >= 0) and (x_index < self.__imageData.shape[1]):
                            currentValue = self.__imageData[y_index, x_index]
                            xx           = (int(currentValue) - int(centralValue)) ** 2
                            H[m, n]      = np.exp(-xx / (2 * (r_sigma ** 2)))
                            F[m, n]      = H[m, n] * self.__GaussModel[m, n]
                            B[m, n]      = F[m, n] * currentValue
                self.__imageFiltered[i, j] = np.sum(B) / np.sum(F)


    def __creatGaussModel(self, filModelX, filModelY, s_sigma):
        self.__GaussModel = np.zeros([filModelX, filModelY])
        GaussModelData = open("GaussModelData.txt", 'w+')
        for i in range(filModelX):
            for j in range(filModelY):
                self.__GaussModel[i, j] = np.exp(-((i - 7) ** 2 + (j - 7) ** 2)
                    / (2 * (s_sigma ** 2)))
                print(round(self.__GaussModel[i, j], 4), end = "\t", file = GaussModelData)
            print('\n', file = GaussModelData)
        GaussModelData.close()
