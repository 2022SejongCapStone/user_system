import sys
import time
import threading
import cv2
import numpy
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Main(QDialog):
    
    def __init__(self):
        super().__init__()
        self.path = '../src/search.mp4'
        self.initUI()
        self.setValueforWidget()
        self.thread = threading.Thread(target=self.viewVideo, args=[])
        self.thread.daemon = True
        self.thread.start()

    def initUI(self):
        self.main_layout = QVBoxLayout()

        self.frame_1 = QFrame()
        self.frame_1.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame_2 = QFrame()
        self.frame_2.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame_3 = QFrame()
        self.frame_3.setFrameShape(QFrame.Panel | QFrame.Sunken)

        self.layout_1 = QVBoxLayout()
        self.layout_2 = QVBoxLayout()
        self.layout_3 = QVBoxLayout()
        
        self.groupbox_1 = QGroupBox('Incoming Packet Content')
        self.vbox_1 = QVBoxLayout()
        self.label_1 = QLabel('0', self)
        self.vbox_1.addWidget(self.label_1)
        self.groupbox_1.setLayout(self.vbox_1)
        self.layout_2.addWidget(self.groupbox_1)
        
        self.groupbox_2 = QGroupBox('Most Similar File')
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        self.vbox_2 = QVBoxLayout()
        self.label_2 = QLabel('0', self)
        self.label_3 = QLabel('File Name', self)
        self.label_4 = QLabel('0', self)
        self.label_5 = QLabel('Similarity', self)
        self.hbox_1.addWidget(self.label_3)
        self.hbox_1.addWidget(self.label_2)
        self.hbox_2.addWidget(self.label_5)
        self.hbox_2.addWidget(self.label_4)
        self.vbox_2.addLayout(self.hbox_1)
        self.vbox_2.addLayout(self.hbox_2)
        self.groupbox_2.setLayout(self.vbox_2)
        self.layout_2.addWidget(self.groupbox_2)
        
        self.groupbox_3 = QGroupBox('Compute Status')
        self.hbox_3 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        self.vbox_3 = QVBoxLayout()
        self.progress_1 = QProgressBar(self)
        self.label_6 = QLabel('CPU Speed', self)
        self.progress_2 = QProgressBar(self)
        self.label_7 = QLabel('Memory usage', self)
        self.hbox_3.addWidget(self.label_6)
        self.hbox_3.addWidget(self.progress_1)
        self.hbox_4.addWidget(self.label_7)
        self.hbox_4.addWidget(self.progress_2)
        self.vbox_3.addLayout(self.hbox_3)
        self.vbox_3.addLayout(self.hbox_4)
        self.groupbox_3.setLayout(self.vbox_3)
        self.layout_2.addWidget(self.groupbox_3)
        
        self.textedit = QTextEdit()
        self.textedit.setReadOnly(True)
        self.layout_3.addWidget(self.textedit)
        
        self.label_8 = QLabel()
        self.layout_1.addWidget(self.label_8)

        self.frame_1.setLayout(self.layout_1)
        self.frame_2.setLayout(self.layout_2)
        self.frame_3.setLayout(self.layout_3)

        self.spliter_1 = QSplitter(Qt.Horizontal)
        self.spliter_1.addWidget(self.frame_1)
        self.spliter_1.addWidget(self.frame_2)

        self.spliter_2 = QSplitter(Qt.Vertical)
        self.spliter_2.addWidget(self.spliter_1)
        self.spliter_2.addWidget(self.frame_3)
        
        self.spliter_1.setSizes([1500, 420])
        self.spliter_2.setSizes([800, 280])

        self.main_layout.addWidget(self.spliter_2)

        self.setLayout(self.main_layout)
        self.setWindowTitle('DarkWeb Monitoring System User View')
        self.showMaximized()
        
        
    def setValueforWidget(self):
        self.progress_1.setValue(80)
        self.progress_2.setValue(50)
        
        
    def viewVideo(self):
        cap = cv2.VideoCapture(self.path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        sleep_ms = int(numpy.round((1 / fps) * 500))
        while True:
            ret, frame = cap.read()
            if ret:
                rgbimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, c = rgbimage.shape
                qimg = QImage(rgbimage.data, w, h, w * c, QImage.Format_RGB888)
                pixmap = QPixmap(qimg)
                
                p = pixmap.scaled(1400, 700, Qt.IgnoreAspectRatio)
                self.label_8.setPixmap(p)
                self.label_8.update()
                if cv2.waitKey(sleep_ms) == ord('q'):
                    break
            else:
                cap = cv2.VideoCapture(self.path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                sleep_ms = int(numpy.round((1 / fps) * 500))
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())