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
import time
from qt_material import apply_stylesheet

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
accesss_key = 'OTOSP4zl6AHejEc10Bj7'
secret_key = 'FNzp5yHsjUgIGa2Uk9uTTZTRUZ4bGAPEWxhtjtiL'

s3= boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=accesss_key,
                     aws_secret_access_key=secret_key)

bucket_name = 'dwkrefrigerator'
    
object_name = 'refrigerator_image'
folder_path = './input_image'
local_file_path = os.path.join(folder_path, 'output.png')

ui = uic.loadUiType('./ref_sys_1.ui')[0]

frame_table = np.zeros((480, 640))


class VideoThread(QThread):
    change_pixmap_signal_image = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            s3.download_file(bucket_name, 'fridge_frame', './cloud/fridge_frame.png')
            s3.download_file(bucket_name, 'table_frame', './cloud/table_frame.png')
            s3.download_file(bucket_name, 'receipt_image', './cloud/receipt_image.png')
            s3.download_file(bucket_name, 'fridge_list', './cloud/fridge_list.txt')
            s3.download_file(bucket_name, 'table_list', './cloud/table_list.txt')
            
            fridge_frame = cv2.imread('./cloud/fridge_frame.png')
            table_frame = cv2.imread('./cloud/table_frame.png')
            receipt_image = cv2.imread('./cloud/receipt_image.png')
            
            fridge_file = open("./cloud/fridge_list.txt")
            table_file = open("./cloud/table_list.txt")
            fridge_list = fridge_file.read()
            table_list = table_file.read()
            fridge_file.close()
            table_file.close()
            
            self.change_pixmap_signal_image.emit([fridge_frame, table_frame, receipt_image, fridge_list, table_list])
            cv2.waitKey(33)
            
class App(QWidget, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal_image.connect(self.update_image)
        # start the thread
        self.thread.start()

    @pyqtSlot(list)
    def update_image(self, data_list):
        """Updates the image_label with a new opencv image"""
        fridge_frame = self.convert_cv_qt(data_list[0])
        table_frame = self.convert_cv_qt(data_list[1])
        receipt_image = self.convert_cv_qt(data_list[2])
        
        food_list = ''.join(data_list[3:])
        
        self.label_fridge_frame.setPixmap(fridge_frame)
        self.label_table_frame.setPixmap(table_frame)
        self.label_receipt_frame.setPixmap(receipt_image)
        self.label_food_list.setText(food_list)
        
        
    def convert_cv_qt(self, frame):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(538, 400, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
#    apply_stylesheet(app, theme='dark_teal.xml')
    a.show()
    sys.exit(app.exec_())