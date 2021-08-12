from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from PyQt5 import uic
import boto3
import os

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
accesss_key = 'OTOSP4zl6AHejEc10Bj7'
secret_key = 'FNzp5yHsjUgIGa2Uk9uTTZTRUZ4bGAPEWxhtjtiL'

s3= boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=accesss_key,
                     aws_secret_access_key=secret_key)

bucket_name = 'dwkrefrigerator'
    
object_name = 'refrigerator_image'
local_file_path = './image/output.png'

ui = uic.loadUiType('./ref_sys_1.ui')[0]

frame_table = np.zeros((480, 640))

class VideoThread(QThread):
    global frame_table
    change_pixmap_signal_ref = pyqtSignal(np.ndarray)
    change_pixmap_signal_tab = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        while True:
            ret, frame = cap.read()
            if ret:
                self.change_pixmap_signal_ref.emit(frame)
            if not os.path.isfile('./image/output.png'):
                s3.download_file(bucket_name, object_name, local_file_path)
                frame_table = cv2.imread('./image/output.png')
                os.remove('./image/output.png')
            self.change_pixmap_signal_tab.emit(frame_table)
        # shut down capture system
        cap.release()
class App(QWidget, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal_ref.connect(self.update_image_ref)
        self.thread.change_pixmap_signal_tab.connect(self.update_image_tab)
        # start the thread
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image_ref(self, frame):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(frame)
        self.label_refrigerator_frame.setPixmap(qt_img)
        
    @pyqtSlot(np.ndarray)
    def update_image_tab(self, frame):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(frame)
        self.label_table_frame.setPixmap(qt_img)
    
    def convert_cv_qt(self, frame):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(538, 400, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    s3.download_file(bucket_name, object_name, local_file_path)
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())