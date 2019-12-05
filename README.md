# BilateralFilter_PyQt5_CUDA
### -*- coding: utf-8 -*-
### Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
### Author             : luoshutu.

## 运行环境
    Win10 + Python3.6.5 + cuda9.2 + cudnn7.6.4 + PyQt5

## 使用
    1、运行: python main.py。
    2、点击选择-->加载图片-->选择一张图片(格式可为jpg、gif、png、jpeg)。
    3、点击滤波，得到结果。

## 文件说明
    1、main.py                :程序入口。
    2、window.ui              :使用Qt Creator设计的ui文件。
    3、windowLayout.py        :通过命令pyuic5 -o windowLayout.py window.ui将.ui文件转为.py文件，以便使用。
    4、mainWindow.py          :界面的信号与动作的连接。
    5、bilateralFilter.py     :图像处理
    6、bilateralFilter_cu.py  :cuda核函数

## 注意事项
    1、输入图像将被重设为512x512大小的图像，目前选用函数不恰当，高分辨率图像将会得到很差的结果。
        self.srcImage = self.srcImage.scaled(512, 512, QtCore.Qt.KeepAspectRatio)
    2、传入pycuda的SourceModule中的数据需为float型，否则会出现寻址错误的情况。
    3、使用cuda核函数时，分配block与grid大小的变量应为整型。
    4、使用cuda核函数时，通过drv.In与drv.Out形式传递的参数应为numpy数组形式。
    5、通过import pycuda.autoinit进行pycuda的初始化。
