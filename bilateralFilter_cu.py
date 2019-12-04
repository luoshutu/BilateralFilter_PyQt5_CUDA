# -*- coding: utf-8 -*-
#Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
#Author             : luoshutu.
#Creat CUDA kernel

import pycuda.autoinit
import pycuda.driver as drv
from pycuda import gpuarray, cumath

import numpy as np

class bilFilKernel(object):
    """docstring for bilFilKernel"""
    def __init__(self):
        super(bilFilKernel, self).__init__()

    def creatGaussModel_gpu(self, filModelX, filModelY, s_sigma):
        borderX = int(filModelX / 2)
        borderY = int(filModelY / 2)
        tmpX = np.arange(-borderX, borderX + 1)
        tmpY = np.arange(-borderY, borderY + 1)
        [x, y] = np.meshgrid(tmpX, tmpY)

        device_x = gpuarray.to_gpu(x)
        device_y = gpuarray.to_gpu(y)
        device_X = device_x * device_x
        device_Y = device_y * device_y
        device_GaussModel = cumath.exp(- (device_X + device_Y) / np.float32(2 * s_sigma * s_sigma))
        
        self.__GaussModel = device_GaussModel.get()
        return self.__GaussModel

