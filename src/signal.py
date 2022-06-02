import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class UpdateProgressBar(QObject):
    signal = pyqtSignal()

    def run(self):
        self.signal.emit()
        

class UpdateTextEdit(QObject):
    signal = pyqtSignal()
    
    def run(self):
        self.signal.emit()
        

class UpdateLabel(QObject):
    signal = pyqtSignal()
    
    def run(self):
        self.signal.emit()
