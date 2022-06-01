import sys, os
import time
import threading
import psutil
import cv2
import numpy
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src import jsonmodule as jm
from src import signal


class Main(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.path = '../src/search.mp4'
        self.string = "Test Text"
        self.signalofprogress = signal.UpdateProgressBar()
        self.signalofprogress.signal.connect(self.updateProgressBar)
        self.signaloftextedit = signal.UpdateTextEdit()
        self.signaloftextedit.signal.connect(self.updateTextEdit)
        self.printText("init UI complete")
        self.makeThread()
        self.printText("start Thread")

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
        self.layout_2.setSpacing(20)
        self.layout_3 = QVBoxLayout()
        
        self.font_1 = QFont("MS Reference Sans Serif", 16, QFont.Bold)
        self.font_2 = QFont('Consolas', 16)
        self.font_3 = QFont('Leelawadee UI', 16, QFont.Bold)
        self.font_4 = QFont('Leelawadee UI', 14)
        self.font_5 = QFont('Consolas', 12, QFont.Bold)
        
        self.groupbox_1 = QGroupBox('Incoming Packet Content')
        self.groupbox_1.setFont(self.font_1)
        self.groupbox_1.setStyleSheet("QGroupBox:title {color: rgb(200, 0, 0); background-color: rgb(200, 220, 220); border: 1px solid black;}"
                                      "QGroupBox {border: 1px solid black; background-color: rgb(255, 255, 255);}")
        
        self.vbox_1 = QVBoxLayout()
        self.label_1 = QLabel('0', self)
        self.label_1.setFont(self.font_2)
        self.vbox_1.addWidget(self.label_1)
        self.groupbox_1.setLayout(self.vbox_1)
        self.layout_2.addWidget(self.groupbox_1)
        
        self.groupbox_2 = QGroupBox('Most Similar File')
        self.groupbox_2.setFont(self.font_1)
        self.groupbox_2.setStyleSheet("QGroupBox:title {color: rgb(150, 200, 0); background-color: rgb(200, 220, 220); border: 1px solid black;}"
                                      "QGroupBox {border: 1px solid black; background-color: rgb(255, 255, 255);}")
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        self.vbox_2 = QVBoxLayout()
        self.label_2 = QLabel('0', self)
        self.label_2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_2.setFixedWidth(210)
        self.label_2.setFont(self.font_2)
        self.label_3 = QLabel('File Name', self)
        self.label_3.setFont(self.font_3)
        self.label_4 = QLabel('0', self)
        self.label_4.setStyleSheet("QLabel {color: rgb(255, 0, 0);}")
        self.label_4.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_4.setFixedWidth(210)
        self.label_4.setFont(self.font_2)
        self.label_5 = QLabel('Similarity', self)
        self.label_5.setFont(self.font_3)
        self.label_5.setStyleSheet("QLabel {color: rgb(255, 0, 0);}")
        self.hbox_1.addWidget(self.label_3)
        self.hbox_1.addWidget(self.label_2)
        self.hbox_2.addWidget(self.label_5)
        self.hbox_2.addWidget(self.label_4)
        self.vbox_2.addLayout(self.hbox_1)
        self.vbox_2.addLayout(self.hbox_2)
        self.groupbox_2.setLayout(self.vbox_2)
        self.layout_2.addWidget(self.groupbox_2)
        
        self.groupbox_3 = QGroupBox('Compute Status')
        self.groupbox_3.setFont(self.font_1)
        self.groupbox_3.setStyleSheet("QGroupBox:title {color: rgb(0, 130, 130); background-color: rgb(200, 220, 220); border: 1px solid black;}"
                                      "QGroupBox {border: 1px solid black; background-color: rgb(255, 255, 255);}")
        self.hbox_3 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        self.vbox_3 = QVBoxLayout()
        self.progress_1 = QProgressBar(self)
        self.progress_1.setFixedWidth(200)
        self.progress_1.setStyleSheet("""
                                    QProgressBar {
                                    background-color: #C0C6CA;
                                    height: 40px;
                                    }
                                    QProgressBar:chunk {
                                    background: #7D94B0;
                                    }
                                    """)
        self.progress_1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_6 = QLabel('CPU usage', self)
        self.label_6.setStyleSheet("QLabel {margin-bottom: 6px;}")
        self.label_6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_6.setFont(self.font_4)
        self.progress_2 = QProgressBar(self)
        self.progress_2.setFixedWidth(200)
        self.progress_2.setStyleSheet("""
                                    QProgressBar {
                                    background-color: #C0C6CA;
                                    height: 40px;
                                    }
                                    QProgressBar:chunk {
                                    background: #7D94B0;
                                    }
                                    """)
        self.progress_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_7 = QLabel('Memory usage', self)
        self.label_7.setStyleSheet("QLabel {margin-bottom: 6px;}")
        self.label_7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_7.setFont(self.font_4)
        self.hbox_3.addWidget(self.label_6)
        self.hbox_3.addWidget(self.progress_1)
        self.hbox_4.addWidget(self.label_7)
        self.hbox_4.addWidget(self.progress_2)
        self.vbox_3.addLayout(self.hbox_3)
        self.vbox_3.addLayout(self.hbox_4)
        self.groupbox_3.setLayout(self.vbox_3)
        self.layout_2.addWidget(self.groupbox_3)
        
        self.textedit = QTextEdit()
        self.textedit.setStyleSheet("QTextEdit {background-color: rgb(0, 0, 0); color: rgb(0, 255, 0);}")
        self.textedit.setFont(self.font_5)
        self.textedit.setReadOnly(True)
        self.layout_3.addWidget(self.textedit)
        
        self.label_8 = QLabel()
        self.label_8.setAlignment(Qt.AlignCenter)
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
        return
        
        
    def makeThread(self):
        self.videothread = threading.Thread(target=self.viewVideoFlow, args=[])
        self.videothread.daemon = True
        self.computethread = threading.Thread(target=self.setComputeValueFlow, args=[])
        self.computethread.daemon = True
        self.socketthread = threading.Thread(target=self.clientSocketFlow, args=[])
        self.socketthread.daemon = True
        self.videothread.start()
        self.computethread.start()
        self.socketthread.start()
        return
        
        
    def setComputeValueFlow(self):
        while True:
            self.signalofprogress.run()
            time.sleep(1)
        return
        
        
    def viewVideoFlow(self):
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
                
                p = pixmap.scaled(1500, 800, Qt.IgnoreAspectRatio)
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
        return
    
    
    def clientSocketFlow(self):
        return
    
    
    def printText(self, string):
        self.string = string
        self.signaloftextedit.run()
        return
        

    @pyqtSlot()
    def updateProgressBar(self):
        cpu = int(psutil.cpu_percent())
        memory = int(psutil.virtual_memory().percent)
        self.progress_1.setValue(cpu)
        self.progress_2.setValue(memory)
    
    @pyqtSlot()
    def updateTextEdit(self):
        self.textedit.append(self.string)
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())