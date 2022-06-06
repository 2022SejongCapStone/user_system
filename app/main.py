from re import S
import sys, os
import time
import threading
import psutil
import socket
import cv2
import numpy
import pickle
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src import jsonmodule as jm
from src import signal
from src import AdditiveElgamal as ae
from src import compare as cp
from src import report as rp
from src import message as ma

content = '''
<h1>파일 유출이 탐지되었습니다!</h1>
<h2>지금 바로 첨부된 파일을 열어 유출된 파일 정보를 확인하시길 바랍니다!</h2><br><br><br><br>


저희 서비스를 사용해주셔서 감사합니다!<br>
저희는 세종대학교 정보보호학과 뭉게구름입니다😊
'''

class Main(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.host = jm.get_secret("SERVERIP")
        self.port = jm.get_secret("SERVERPORT")
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.path = '../src/search.mp4'
        self.string = "Test Text"
        self.labelstring1 = ""
        self.labelstring2 = ""
        self.labelstring3 = ""
        self.signalofprogress = signal.UpdateProgressBar()
        self.signalofprogress.signal.connect(self.updateProgressBar)
        self.signaloftextedit = signal.UpdateTextEdit()
        self.signaloftextedit.signal.connect(self.updateTextEdit)
        self.signaloflabel1 = signal.UpdateLabel()
        self.signaloflabel1.signal.connect(self.updateLabel1)
        self.signaloflabel2 = signal.UpdateLabel()
        self.signaloflabel2.signal.connect(self.updateLabel2)
        self.signaloflabel3 = signal.UpdateLabel()
        self.signaloflabel3.signal.connect(self.updateLabel3)
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
        self.label_1 = QLabel('-', self)
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
        self.label_2 = QLabel('-', self)
        self.label_2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_2.setFixedWidth(210)
        self.label_2.setFont(self.font_2)
        self.label_3 = QLabel('File Name', self)
        self.label_3.setFont(self.font_3)
        self.label_4 = QLabel('-', self)
        self.label_4.setStyleSheet("QLabel {color: rgb(255, 0, 0);}")
        self.label_4.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_4.setFixedWidth(210)
        self.label_4.setFont(self.font_2)
        self.label_5 = QLabel('Code Line', self)
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
        path = self.path
        cap = cv2.VideoCapture(path)
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
            elif ret != True and path == "../src/search.mp4":
                cap = cv2.VideoCapture(path)
            if self.path != path:
                path = self.path
                cap = cv2.VideoCapture(path)
        cap.release()
        cv2.destroyAllWindows()
        return


    def clientSocketFlow(self):
        try:
            self.clientsocket.connect((self.host, self.port))
            publickey = pickle.loads(self.clientsocket.recv(1500))
            self.printText("Get public key from server")
            self.pubkey = ae.construct_additive((publickey['P'], publickey['G'], publickey['Y']))
            while True:
                self.printText("Server now searching new files")
                self.path = '../src/search.mp4'
                server_enc_simhash_list = []
                count = self.clientsocket.recv(10)
                self.path = '../src/found.mp4'
                count = count.strip(b'A')
                self.printText("File Found on Dark Web")
                print("Good!: " + str(count))
                count = int(count)
                for i in range(count):
                    data = []
                    while True:
                        packet = self.clientsocket.recv(1500)
                        if b"EndofPacket" == packet:
                            break
                        data.append(packet)
                    self.printText("Fragment Get")
                    data_arr = pickle.loads(b"".join(data))
                    server_enc_simhash_list.append(data_arr)
                enc_HD_dict = {}
                with open('../test.p','rb') as f:
                    obj = pickle.load(f)
                    #Start Comparing process
                self.printText("COMPARING START!...")
                enc_HD_dict_list = []
                for data in server_enc_simhash_list:
                    enc_HD_dict = {} # k,v = reprisentative_id , enc_HD
                    server_idx = list(data.keys())[0]
                    enc_server_simhash = list(data.values())[0]

                    for idx, val in obj.items(): 
                        if not (idx == server_idx):
                            continue
                        for representative_cfid, cloneclass in val.items():
                            for cfid, code_fragment in cloneclass.items():
                                if not ( cfid == representative_cfid):
                                    continue
                                simhash = code_fragment[3]
                                enc_HD_dict[representative_cfid] = cp.get_enc_HD(self.pubkey, simhash, enc_server_simhash)
                                self.printLabel1(str(enc_HD_dict[representative_cfid])[:25] +
                                                 "\n" + 
                                                 str(enc_HD_dict[representative_cfid])[25:50] +
                                                 "\n" + 
                                                 str(enc_HD_dict[representative_cfid])[50:75] +
                                                 "\n" +
                                                 str(enc_HD_dict[representative_cfid])[75:100] +
                                                 "...")
                        break
                    enc_HD_dict_list.append(enc_HD_dict)
                self.printText("send sim value to server(encrypt)")
                self.path = '../src/sendsimvalue.mp4'
                self.clientsocket.sendall(pickle.dumps(enc_HD_dict_list))
                time.sleep(1)
                self.clientsocket.sendall("EndofPacket".encode())
                time.sleep(1)
                absence = self.clientsocket.recv(10)
                print(str(absence))
                if b"YYYYYYYYYY" == absence:
                    self.printText("WARNING!")
                    self.path = '../src/highsimilarity.mp4'
                    data = []
                    while True:
                        packet = self.clientsocket.recv(1500)
                        if b"EndofPacket" == packet:
                            break
                        data.append(packet)
                    reportdict = pickle.loads(b"".join(data))
                    for idx, val in obj.items(): 
                        for representative_cfid, cloneclass in val.items():
                            #for cfid, code_fragment in cloneclass.items():
                            if representative_cfid == reportdict["clnt_cfid"]:
                                reportdict["clnt_cloneclass"] = cloneclass
                                # reportdict["clnt_file"] = code_fragment[1]
                                # reportdict["clnt_startline"] = code_fragment[0]
                                # reportdict["clnt_endline"] = code_fragment[2]
                                self.path = '../src/request.mp4'
                                break
                    self.printLabel2(reportdict["clnt_cloneclass"][reportdict["clnt_cfid"]][1][:15] + "\n" + 
                                     reportdict["clnt_cloneclass"][reportdict["clnt_cfid"]][1][15:])
                    self.printLabel3(str(reportdict["clnt_cloneclass"][reportdict["clnt_cfid"]][0]) + "~" + str(reportdict["clnt_cloneclass"][reportdict["clnt_cfid"]][2]))
                    self.printText("print all of data\n")
                    htmlreport = ma.getHTMLCloneDOM(reportdict)
                    with open("../report/reportfile.html", "w") as f:
                        f.write(htmlreport)
                    self.emailclient = rp.SMTPclient()
                    self.emailclient.makeBody(content)
                    self.emailclient.attachFile(["../report/reportfile.html"])
                    self.emailclient.sendMail()
                    time.sleep(4)
                    self.printLabel1("-")
                    self.printLabel2("-")
                    self.printLabel3("-")
                else:
                    self.printText("there is no file in our system\n")
                    self.path = '../src/lowsimilarity.mp4'
                    time.sleep(4)
                    continue
        except Exception as e:
            print("Error", e)
            self.clientsocket.close()
            return


    def printText(self, string):
        self.string = string
        self.signaloftextedit.run()
        return


    def printLabel1(self, string):
        self.labelstring1 = string
        self.signaloflabel1.run()
        return


    def printLabel2(self, string):
        self.labelstring2 = string
        self.signaloflabel2.run()
        return


    def printLabel3(self, string):
        self.labelstring3 = string
        self.signaloflabel3.run()
        return


    @pyqtSlot()
    def updateProgressBar(self):
        cpu = int(psutil.cpu_percent())
        memory = int(psutil.virtual_memory().percent)
        self.progress_1.setValue(cpu)
        self.progress_2.setValue(memory)


    @pyqtSlot()
    def updateTextEdit(self):
        self.textedit.append(time.strftime('%Y-%m-%d', time.localtime(time.time())) + time.strftime(' %c', time.localtime(time.time())) + " - INFO [{}]".format(os.path.basename(__file__)) + self.string)


    @pyqtSlot()
    def updateLabel1(self):
        self.label_1.setText(str(self.labelstring1))


    @pyqtSlot()
    def updateLabel2(self):
        self.label_2.setText(str(self.labelstring2))


    @pyqtSlot()
    def updateLabel3(self):
        self.label_4.setText(str(self.labelstring3))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    #main.show()
    sys.exit(app.exec_())
