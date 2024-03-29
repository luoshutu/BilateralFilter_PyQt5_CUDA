# -*- coding: utf-8 -*-
#Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
#Author             : luoshutu.
#Creat QT Application.

# 配置pycuda的运行环境
from __future__ import print_function
from __future__ import absolute_import
import pycuda.tools
import pycuda.autoinit

from PyQt5 import QtCore, QtGui

import pycuda.driver as drv
import numpy as np
import time

import bilateralFilter_cu as BFCU

class bilateralFilter(object):
    """docstring for bilateralFilter"""
    def __init__(self):
        super(bilateralFilter, self).__init__()
        self.__imageFiltered = np.array
        self.__imageData     = np.array
        self.__GaussModel    = np.array

    def getImageAndFilterParameter(self, inputImage, filModelX, filModelY, s_sigma, r_sigma):
        self.__imageData = self.qimageToNumpy(inputImage)                                               #将QImage形式的图像转化为Numpy矩阵形式
        self.__imageFiltered = np.zeros([self.__imageData.shape[0], self.__imageData.shape[1]])         #初始化一个与输入图像大小一致的数据缓存区

        filterStartTime = time.time()                                                                   #开启计时器
        self.__filter_gpu(filModelX, filModelY, s_sigma, r_sigma)                                       #使用gpu进行滤波
        filterStopTime  = time.time()                                                                   #关闭计时器
        self.cpuFilterTime = filterStopTime - filterStartTime                                           #得到运行时间
        print('FilterTime:', self.cpuFilterTime)

    #将滤波过后的数据转换为QImage的形式，并传输出去
    def getFilteredImage(self):
        #print(self.__imageFiltered)
        outputImage = QtGui.QImage(self.__imageFiltered, self.__imageFiltered.shape[1], 
            self.__imageFiltered.shape[0], QtGui.QImage.Format_Grayscale8) 
        return outputImage, self.cpuFilterTime

    #将QImage形式数据转化为Numpy矩阵
    def qimageToNumpy(self, qimage):
        imageTemp = qimage.constBits()
        imageTemp.setsize(qimage.byteCount())
        result = np.array(imageTemp).reshape(qimage.height(), qimage.width())
        print(result.shape)
        return result

    #使用CPU的方式进行滤波
    def __filter_cpu(self, filModelX, filModelY, s_sigma, r_sigma):
        self.__creatGaussModel(filModelX, filModelY, s_sigma)
        self.__imageFiltered = self.__imageFiltered.astype(np.uint8)                                    #将数据类型转换为8位的无符号整型
        for i in range(self.__imageData.shape[0]):
            for j in range(self.__imageData.shape[1]):
                H = np.zeros([filModelX, filModelY])
                B = np.zeros([filModelX, filModelY])
                F = np.zeros([filModelX, filModelY])
                centralValue = self.__imageData[i, j]                                                   #滤波时，位于滤波核的中心的图像值
                for m in range(filModelX):
                    for n in range(filModelY):
                        y_index = i + m - 7
                        x_index = j + n - 7
                        if (y_index >= 0) and (y_index < self.__imageData.shape[0]) and \
                        (x_index >= 0) and (x_index < self.__imageData.shape[1]):
                            currentValue = self.__imageData[y_index, x_index]                           #滤波运算时，滤波核遍历时的当前值
                            xx           = (float(currentValue) - float(centralValue)) ** 2
                            H[m, n]      = np.exp(-xx / (2 * (r_sigma ** 2)))
                            F[m, n]      = H[m, n] * self.__GaussModel[m, n]
                            B[m, n]      = F[m, n] * currentValue
                self.__imageFiltered[i, j] = np.sum(B) / np.sum(F)

    #使用CPU计算一个高斯滤波核
    def __creatGaussModel(self, filModelX, filModelY, s_sigma):
        self.__GaussModel = np.zeros([filModelX, filModelY])
        #GaussModelData = open("GaussModelData.txt", 'w+')
        for i in range(filModelX):
            for j in range(filModelY):
                self.__GaussModel[i, j] = np.exp(-((i - int(filModelX / 2)) ** 2 
                                                 + (j - int(filModelY / 2)) ** 2)
                                                 /(2 * (s_sigma ** 2)))
                #print(round(self.__GaussModel[i, j], 4), end = "\t", file = GaussModelData)
            #print('\n', file = GaussModelData)
        #GaussModelData.close()

    #使用GPU方式进行滤波
    def __filter_gpu(self, filModelX, filModelY, s_sigma, r_sigma):
        self.__GaussModel = np.zeros([filModelX, filModelY])
        self.__GaussModel = self.__GaussModel.astype(np.float32)

        #self.__creatGaussModel(filModelX, filModelY, s_sigma)

        #使用cuda计算出一个高斯核
        s_sigma     = np.array([s_sigma]).astype(np.float32)
        filModelLen = np.array([filModelX]).astype(np.uint8)
        BFCU.creatGaussModel(drv.Out(self.__GaussModel), drv.In(s_sigma), drv.In(filModelLen), 
                             block = (filModelX, filModelY, 1), grid = (1, 1))
        #print(self.__GaussModel)


        r_sigma   = np.array([r_sigma]).astype(np.float32)
        #print(r_sigma)
        imgWidth  = np.array([self.__imageData.shape[1]]).astype(np.uint16)                             #注意数据类型，以免图像大小溢出
        imgHeight = np.array([self.__imageData.shape[0]]).astype(np.uint16)
        #print('width',imgWidth,self.__imageData.shape[1])
        #print('height',imgHeight,self.__imageData.shape[0])
        blockSizeDim1 = int(32)                                                                         #分配block以及gird的大小的数据类型应为整型
        blockSizeDim2 = int(32)
        gridSizeDim1  = int(imgWidth[0]  / blockSizeDim1)
        gridSizeDim2  = int(imgHeight[0]  / blockSizeDim2)

        self.__imageFiltered = self.__imageFiltered.astype(np.float32)                                  #传入GPU中计算的数据最好为float型，否则会出现奇怪的错误
        self.__imageData = self.__imageData.astype(np.float32)
        BFCU.bilateral_filter_kernel(drv.Out(self.__imageFiltered), drv.In(self.__imageData), drv.In(self.__GaussModel),
                             drv.In(imgWidth), drv.In(imgHeight), drv.In(r_sigma), drv.In(filModelLen), 
                             block = (blockSizeDim1, blockSizeDim2, 1), grid = (gridSizeDim1, gridSizeDim2))
        self.__imageFiltered = self.__imageFiltered.astype(np.uint8)
        #print(self.__imageFiltered)
