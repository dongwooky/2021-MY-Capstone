from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from PyQt5 import uic

ui = uic.loadUiType('./ref_sys_1.ui')[0]

class MyApp(QWidget, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp() 
    ex.show()
    app.exec_()