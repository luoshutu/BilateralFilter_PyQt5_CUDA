# -*- coding: utf-8 -*-
#Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
#Author             : luoshutu.
#Creat QT Application.

from PyQt5 import QtWidgets
import mainWindow as mw

def main():
    app = QtWidgets.QApplication([])

    m = mw.MainWindow()

    app.exec_()

if __name__ == "__main__":
    main()

