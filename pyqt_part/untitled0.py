from PyQt5.QtWidget import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys

class myapp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('basic location')
        self.setWindowIcon(QIcon('igm/'))