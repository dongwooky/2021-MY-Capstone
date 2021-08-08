import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap


changePixmap = pyqtSignal(QImage)


capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print('Camera open failed!')
    sys.exit()
while True:
    ret, frame = capture.read()
    if not ret:
        print('Frame read error!')
        sys.exit()
    frame = cv2.resize(frame, dsize=(538, 400), interpolation=cv2.INTER_AREA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, c = frame.shape
    convertToQtFormat = QImage(frame.data, w, h, c * w, QImage.Format_RGB888)
    p = convertToQtFormat.scaled(538, 400, Qt.KeepAspectRatio)
    changePixmap.emit(p)
 