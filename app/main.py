import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        frame_1 = QFrame()
        frame_1.setFrameShape(QFrame.Panel | QFrame.Sunken)
        frame_2 = QFrame()
        frame_2.setFrameShape(QFrame.Panel | QFrame.Sunken)
        frame_3 = QFrame()
        frame_3.setFrameShape(QFrame.Panel | QFrame.Sunken)

        layout_1 = QVBoxLayout()
        layout_2 = QVBoxLayout()
        layout_3 = QVBoxLayout()
        layout_4 = QVBoxLayout()

        # button_1 = QPushButton("button_1")
        # button_2 = QPushButton("button_2")
        # button_3 = QPushButton("button_3")
        
        table = self.make_table()
        layout_4.addWidget(table)
        
        layout_2.addLayout(layout_4)

        # layout_1.addWidget(button_1)
        # layout_2.addWidget(button_2)
        # layout_3.addWidget(button_3)

        frame_1.setLayout(layout_1)
        frame_2.setLayout(layout_2)
        frame_3.setLayout(layout_3)

        spliter_1 = QSplitter(Qt.Horizontal)
        spliter_1.addWidget(frame_1)
        spliter_1.addWidget(frame_2)

        spliter_2 = QSplitter(Qt.Vertical)
        spliter_2.addWidget(spliter_1)
        spliter_2.addWidget(frame_3)
        
        spliter_1.setSizes([1500, 420])
        spliter_2.setSizes([800, 280])

        main_layout.addWidget(spliter_2)

        self.setLayout(main_layout)
        self.setWindowTitle('DarkWeb Monitoring System User View')
        # self.resize(1920, 1080)
        # self.show()
        self.showMaximized()
        
    def make_table(self):
        table = QTableWidget(self)
        table.resize(300, 200)
        # 표의 크기를 지정
        table.setColumnCount(1)
        table.setRowCount(5)
        # 제목 지정
        table.horizontalHeader().setVisible(False)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.setVerticalHeaderLabels(
            ['파일 이름', '수신 데이터', '발견한 URL', '비교 대상', '유사도']
        )

        # 셀 내용 채우기
        table.setItem(0, 0, QTableWidgetItem('test.cpp'))
        table.setItem(1, 0, QTableWidgetItem('1010101001001...'))
        table.setItem(2, 0, QTableWidgetItem('http://123.123.123.123:5000'))
        table.setItem(3, 0, QTableWidgetItem('comparison.cpp'))
        table.setItem(4, 0, QTableWidgetItem('0.7'))
        
        return table

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())