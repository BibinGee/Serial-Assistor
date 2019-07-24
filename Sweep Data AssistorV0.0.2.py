from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import serial
import random
import time

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Serial Assistor V 0.2 Author Daniel Gee')
##        self.title = 'File Translator'
        self.setGeometry(100,100,800,500)
        self.initGui()

    def initGui(self):
        layout = QVBoxLayout()

        h1 = QHBoxLayout()
        self.label1 = QLabel(self)
        self.label1.setText('Serial port')
        h1.addWidget(self.label1)                    
        self.edit1 = QLineEdit(self)
        h1.addWidget(self.edit1)
        layout.addLayout(h1)

        h2 = QHBoxLayout()
        self.label2 = QLabel(self)
        self.label2.setText('Baudrate')
        h2.addWidget(self.label2)                    
        self.edit2 = QLineEdit(self)
        h2.addWidget(self.edit2)
        layout.addLayout(h2)

        h3 = QHBoxLayout()
        self.label5 = QLabel(self)
        self.label5.setText('Step')
        h3.addWidget(self.label5)
        
        self.combox = QComboBox()
        self.combox.addItems(['0.5', '1.0', '2.0', '3.0', '4.0', '5.0'])
        h3.addWidget(self.combox)
        
        self.edit4 = QLineEdit(self)
        h3.addWidget(self.edit4)                 
        self.comBtn = QPushButton('Send command', self)
        self.comBtn.clicked.connect(self.on_click_cmd)
        h3.addWidget(self.comBtn)
        layout.addLayout(h3)

        h2 = QHBoxLayout()
        self.saveBtn = QPushButton('Save', self)
        self.saveBtn.clicked.connect(self.on_click_save)
        h2.addWidget(self.saveBtn)

        self.startBtn = QPushButton('Start', self)
        self.startBtn.clicked.connect(self.on_click_start)
        h2.addWidget(self.startBtn)

        self.pauseBtn = QPushButton('Pause', self)
        self.pauseBtn.clicked.connect(self.on_click_pause)
        h2.addWidget(self.pauseBtn)

        self.recordBtn = QPushButton('Record', self)
        self.recordBtn.setEnabled(False)
        self.recordBtn.clicked.connect(self.on_click_record)
        h2.addWidget(self.recordBtn)

        layout.addLayout(h2)

        self.fnfiled = QLineEdit(self)
        self.fnfiled.setEnabled(False)
        layout.addWidget(self.fnfiled)

        self.tedit = QTextEdit()
        f = self.tedit.font()
        f.setPointSize(11)
        self.tedit.setFont(f)
        layout.addWidget(self.tedit)

        self.edit3 = QLineEdit(self)
        f = self.edit3.font()
        f.setPointSize(12)
        self.edit3.setFont(f)
        self.edit3.setStyleSheet("color: green;")
        self.edit3.setText('......')
        self.edit3.setEnabled(False)
        layout.addWidget(self.edit3)
        
        self.setLayout(layout)
        
        self.ser = serial.Serial ()
        self.file = ''

        self.timer = QBasicTimer()
        self.timer.start(100, self)

        self.characters = list()
        self.line = ''
        self.count = 100.0
        self.flag = False

    @pyqtSlot()
    def on_click_save(self):
        self.file, _ = QFileDialog.getSaveFileName(self, 'Save file', '', 'csv(*.csv)')
        if self.file is not None:
            self.recordBtn.setEnabled(True)
            self.fnfiled.setText(self.file)
        print(self.file)

    @pyqtSlot()
    def on_click_start(self):
        
        if self.edit2.text() is not '':
            print(self.edit2.text())
            self.ser.baudrate = self.edit2.text()
        if self.edit1.text() is not '':
            print(self.edit1.text())
            self.ser.port  = self.edit1.text()

        if self.ser.baudrate and self.ser.port is not None:
            self.ser.timeout = 0.5
            try:
                self.startBtn.setEnabled(False)
                self.edit1.setEnabled(False)
                self.edit2.setEnabled(False)
                self.ser.open()
                print(self.ser.port, 'opened')
                self.flag = True
            except serial.serialutil.SerialException as e:
                print(e)
                self.ser.close()
                self.startBtn.setEnabled(True)
                self.edit1.setEnabled(True)
                self.edit2.setEnabled(True)
                self.flag = False

    @pyqtSlot()
    def on_click_pause (self):
        self.count = 100.0
        self.characters = []
        self.edit3.setText('')
        if self.ser.isOpen ():
            self.ser.close()
            self.flag = False
            self.startBtn.setEnabled(True)
        
    @pyqtSlot()
    def on_click_record(self):
##        print(self.ser.isOpen ())
        step = float(self.combox.currentText())
##        print(step)
        if self.ser.isOpen ():
            print(self.line, 'record')
            if self.file is not '':
                if self.line is not '':
                    self.line = str(self.count) + ': ' + self.line
                    
                    self.count = round((self.count - step), 2)
                    
                    with open(self.file, 'a+') as f:
                            f.write(self.line)
                            f.write('\n')
                    self.edit3.setText(self.line)
                    self.line = ''
                    
    @pyqtSlot()
    def on_click_cmd (self):
        if self.ser.isOpen ():
            cmd = self.edit4.text() + '\r'
            print(cmd.encode())
            self.ser.write(cmd.encode())
            color = QColor(random.randint (0,255), random.randint (0,255), random.randint (0,255))
            self.tedit.setTextColor(color)
            self.tedit.append(self.edit4.text())


    def timerEvent(self, event):

        t = time.strftime ('[%H:%M:%S] ', time.localtime ())
        if self.flag:
            c = self.ser.read()
            try:
                c = c.decode("utf-8", errors = 'replace')
            except UnicodeEncodeError:
                print('decoding error:', c)
##                print('decoding:', c, 'error:', e)
                c = ''

            if  c is not '':
                self.timer.stop()
                et = 0
                while True:
                    if c is not '\n' and c is not '\r' and c is not '':
                        self.characters.append(c)
                    else:
                        if len(self.characters) > 2:
                            print(self.characters)
                            self.line = ''.join(self.characters)
                            color = QColor(random.randint (0,255), random.randint (0,255), random.randint (0,255))
                            self.tedit.setTextColor(color)
                            self.tedit.append(t + self.line)
                            self.tedit.moveCursor(QTextCursor.End)
                            self.characters = []
                        break
                    c = self.ser.read()
                    try:
                        c = c.decode("utf-8", errors = 'replace')
                    except UnicodeEncodeError:
##                        print('decoding:', c, 'error:', e)
                        print('decoding error:', c)
                        c = ''
                    if c is '':
                        et = et + 1
                        if et >= 5:
                            break
                self.timer.start(100, self)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
