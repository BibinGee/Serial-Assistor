# coding = utf-8
# this program is create a simply serial data record assistor for FHK product.
# as well as collecting LTC sensitivity data while conducting the sweep test.
# Develop by: Daniel G.
# Date: 2019-07-27

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import serial
import serial.tools.list_ports
import random
import time
import numpy as np
import kalmanfilter

from Graph import Graph
from warnings import catch_warnings

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FHK Sweep Data Assistor Beta V0.9    Copyright@ Daniel Gee')

#         self.setGeometry(100,100,850,500)
##        self.setFixedSize(820,500)
        self.setWindowIcon(QIcon(r'./sweep data.ico'))
        self.initGui()

    def initGui(self):
        # Global layout container
        layout = QVBoxLayout()
        sub_v_layout = QVBoxLayout()
        sub_h_layout = QHBoxLayout()

        # h1 Horizontal Box to include Unit serial port, baudrate components
        h1 = QHBoxLayout()
        self.label1 = QLabel(self)
        self.label1.setText('Unit Serial')
        self.label1.setFont(QFont("Microsoft YaHei"))
        h1.addWidget(self.label1)                    
        self.edit1 = QLineEdit(self)
        self.edit1.setFont(QFont("Microsoft YaHei"))
        h1.addWidget(self.edit1)

        self.label2 = QLabel(self)
        self.label2.setText('Baudrate')
        self.label2.setFont(QFont("Microsoft YaHei"))
        h1.addWidget(self.label2)                    
        self.edit2 = QLineEdit(self)
        self.edit2.setText('19200')
        self.edit2.setFont(QFont("Microsoft YaHei"))
        h1.addWidget(self.edit2)

        self.unit_ser_open = QPushButton('Open', self)
        self.unit_ser_open.setFont(QFont("Microsoft YaHei"))
        self.unit_ser_open.clicked.connect(self.on_click_unit_ser_open)
        h1.addWidget(self.unit_ser_open)
        
        sub_v_layout.addLayout(h1)

        # h2 Horizontal Box to include LTC serial port, baudrate components
        h2 = QHBoxLayout()
        self.LTC_label1 = QLabel(self)
        self.LTC_label1.setText('LTC Serial')
        self.LTC_label1.setFont(QFont("Microsoft YaHei"))
        h2.addWidget(self.LTC_label1)                    
        self.LTC_edit1 = QLineEdit(self)
        self.LTC_edit1.setFont(QFont("Microsoft YaHei"))
        h2.addWidget(self.LTC_edit1)

        self.LTC_label2 = QLabel(self)
        self.LTC_label2.setText('Baudrate')
        self.LTC_label2.setFont(QFont("Microsoft YaHei"))
        h2.addWidget(self.LTC_label2)                    
        self.LTC_edit2 = QLineEdit(self)
        self.LTC_edit2.setText('19200')
        self.LTC_edit2.setFont(QFont("Microsoft YaHei"))
        self.LTC_edit2.setEnabled(False)
        h2.addWidget(self.LTC_edit2)

        self.ltc_ser_open = QPushButton('Open', self)
        self.ltc_ser_open.setFont(QFont("Microsoft YaHei"))
        self.ltc_ser_open.clicked.connect(self.on_click_ltc_ser_open)
        h2.addWidget(self.ltc_ser_open)
                
        sub_v_layout.addLayout(h2)
        
        # h3 Horizontal Box to include Step, Command components
        h3 = QHBoxLayout()
        self.label5 = QLabel(self)
        self.label5.setFont(QFont("Microsoft YaHei"))
        self.label5.setText('LTC Compensation (uA)')
        h3.addWidget(self.label5)
        
        self.LTC_Comp_edit = QLineEdit(self)
        self.LTC_Comp_edit.setText('0.0')
        h3.addWidget(self.LTC_Comp_edit)
        
        self.edit4 = QLineEdit(self)
        h3.addWidget(self.edit4)                 
        self.comBtn = QPushButton('Send command', self)
        self.comBtn.setFont(QFont("Microsoft YaHei"))
        self.comBtn.clicked.connect(self.on_click_cmd)
        h3.addWidget(self.comBtn)
        sub_v_layout.addLayout(h3)

        # h4 Horizontal Box to include Buttons components
        h4 = QHBoxLayout()
        self.saveBtn = QPushButton('Save', self)
        self.saveBtn.setFont(QFont("Microsoft YaHei"))
        self.saveBtn.clicked.connect(self.on_click_save)
        self.saveBtn.setEnabled(False)
        h4.addWidget(self.saveBtn)

        self.startBtn = QPushButton('Start', self)
        self.startBtn.setFont(QFont("Microsoft YaHei"))
        self.startBtn.clicked.connect(self.on_click_start)
        h4.addWidget(self.startBtn)

        self.pauseBtn = QPushButton('Pause', self)
        self.pauseBtn.setFont(QFont("Microsoft YaHei"))
        self.pauseBtn.setEnabled(False)
        self.pauseBtn.clicked.connect(self.on_click_pause)
        h4.addWidget(self.pauseBtn)

        self.graphBtn = QPushButton('Graph', self)
        self.graphBtn.setFont(QFont("Microsoft YaHei"))
        self.graphBtn.clicked.connect(self.on_click_graph)
        h4.addWidget(self.graphBtn)
        
        sub_v_layout.addLayout(h4)
        
        # include vertical layout
        sub_h_layout.addLayout(sub_v_layout)
        
        # include LTC display field
        self.LTC_label = QLabel(self)
        self.LTC_label.setText('100.00')
        self.LTC_label.setFont(QFont("Microsoft YaHei",24,QFont.Bold))
        self.LTC_label.setStyleSheet('border: 5px solid blue;')
        sub_h_layout.addWidget(self.LTC_label)

        layout.addLayout(sub_h_layout)

        # file path display label
        self.fnfiled = QLineEdit(self)
        self.fnfiled.setEnabled(False)
        layout.addWidget(self.fnfiled)

        # Text display field 
        self.tedit = QTextEdit()
        f = self.tedit.font()
        f.setPointSize(9)
        f.setFamily('Microsoft YaHei')
        self.tedit.setFont(f)
        layout.addWidget(self.tedit)

        self.edit3 = QLineEdit(self)
        f = self.edit3.font()
        f.setPointSize(8)
        f.setFamily('Microsoft YaHei')
        self.edit3.setFont(f)
        self.edit3.setStyleSheet("color: green;")
        self.edit3.setText('......')
        self.edit3.setEnabled(False)
        layout.addWidget(self.edit3)
        
        self.setLayout(layout)

        # Global serial handler
        self.ser = serial.Serial ()
        self.LTC_ser = serial.Serial()
        self.file = ''

        # Define timer to loop events
        self.timer = QBasicTimer()
        self.timer.start(100, self)

        # Define a characters container, to store a sentance.
##        self.characters = list()
        self.line = ''
        self.filtering_data = list()

        # Maximum count down number
##        self.count = 100.0

        # Create a Graph
        self.graph = Graph()

        # Define a flag to control serial data reading ON/OFF..
        self.flag = False
        
        # auto fill seril port
        ports = serial.tools.list_ports.comports(include_links=False)
        for port in ports:
            if port.device is not 'COM1':
                self.edit1.setText(port.device)
                break


    # Method to Open Unit Serial Port
    def on_click_unit_ser_open(self):
        # Get baudrate
        if self.edit2.text() is not '':
            print(self.edit2.text())
            self.ser.baudrate = self.edit2.text()
            
        # Get serial port
        if self.edit1.text() is not '':
            print(self.edit1.text())
            self.ser.port  = self.edit1.text()

        if self.ser.baudrate and self.ser.port is not None:
            self.ser.timeout = 0.05
            try:
                self.unit_ser_open.setEnabled(False)
                self.edit1.setEnabled(False)
                self.edit2.setEnabled(False)
                self.ser.open()
                print('Unit Serial Port:', self.ser.port, 'opened')
                
            except serial.serialutil.SerialException as e:
                print(e)
                self.ser.close()
                self.unit_ser_open.setEnabled(True)
                self.edit1.setEnabled(True)
                self.edit2.setEnabled(True)
        else:
            print('Cannot open Unit Serial Port!!!')
            QMessageBox.warning(self, 'warning', 'Cannot open Unit Serial Port!!! Check Serial port if available')
    
                
     # Method to Open LTC Serial Port           
    def on_click_ltc_ser_open(self):
        # Get baudrate
        if self.LTC_edit2.text() is not '':
            print(self.LTC_edit2.text())
            self.LTC_ser.baudrate = self.LTC_edit2.text()
            
        # Get serial port
        if self.LTC_edit1.text() is not '':
            print(self.LTC_edit1.text())
            self.LTC_ser.port  = self.LTC_edit1.text()

        if self.LTC_ser.baudrate and self.LTC_ser.port is not None:
            self.LTC_ser.timeout = 0.05
            try:
                self.ltc_ser_open.setEnabled(False)
                self.LTC_edit1.setEnabled(False)
                self.LTC_edit2.setEnabled(False)
                self.LTC_ser.open()
                print('LTC Reading Serial Port:', self.LTC_ser.port, 'opened')
 
            except serial.serialutil.SerialException as e:
                print(e)
                self.ltc_ser_open.setEnabled(True)
                self.LTC_ser.close()
                self.LTC_edit1.setEnabled(True)
                self.LTC_edit2.setEnabled(True)
        else:
            print('Cannot open LTC Serial Port!!!')
            QMessageBox.warning(self, 'warning', 'Cannot open LTC Serial Port!!! Check Serial port if available')
                
    # Method to Get a file name   
    #@pyqtSlot()
    def on_click_save(self):
        # Get a file handler, file format '*.csv'
        try:
            self.file, _ = QFileDialog.getSaveFileName(self, 'Save file', '', 'csv(*.csv)')
            if self.file is not None:
                self.fnfiled.setText(self.file)
                if not self.LTC_ser.isOpen:
                    with open(self.file, 'a+') as f:
                        f.write('Time, LTC reading(uA), Serial data')
                        f.write('\n')
                else:
                     with open(self.file, 'a+') as f:
                        f.write('Time, Serial data')
                        f.write('\n')    
                self.saveBtn.setEnabled(False)
#             print(self.file)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, 'Warning', e)

    # Method to set 'flag' TRUE.
   # @pyqtSlot()
    def on_click_start(self):
        try:
            if not self.ser.is_open:
                self.on_click_unit_ser_open()
            if not self.LTC_ser.isOpen:
                self.on_click_ltc_ser_open()
                
            self.startBtn.setEnabled(False)
            self.saveBtn.setEnabled(True)
            self.pauseBtn.setEnabled(True)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, 'warning', e)
        self.flag = True

    # Method to Stop Unit Serial Port, LTC Serial Port update
    # 
    
   # @pyqtSlot()
    def on_click_pause (self):
        try:
            # Clear serial character container
    ##        self.characters = []
            self.filtering_data = []
            
            # clear text field
            self.edit3.setText('')
    
            # close unit serial port, enable open button
            if self.ser.isOpen ():
                self.ser.close()
                self.unit_ser_open.setEnabled(True)
                self.edit1.setEnabled(True)
                self.edit2.setEnabled(True)
                
            # close LTC serial port, enable open button   
            if self.LTC_ser.isOpen ():
                self.LTC_ser.close()
                self.ltc_ser_open.setEnabled(True)
                self.LTC_edit1.setEnabled(True)
                self.LTC_edit2.setEnabled(True)
            # disable event loop
            self.flag = False
    
            # enable start button
            self.startBtn.setEnabled(True)
            
            # enable save button
            self.saveBtn.setEnabled(True)
            
            self.pauseBtn.setEnabled(False)
    
            # Clear file path
            self.file = ''
            self.fnfiled.setText('')
        except Exception as e:
            print(e)
            QMessageBox.warning(self, 'Warning', e)



    # Send command to Unit through Unit Serial Port                
   
    #@pyqtSlot()
    def on_click_cmd (self):
        if self.ser.isOpen ():
            cmd = self.edit4.text() + '\r'
#             print(cmd.encode())
            
            # send command through serial port
            self.ser.write(cmd.encode())
#             color = QColor(random.randint (0,255), random.randint (0,255), random.randint (0,255))
#             self.tedit.setTextColor(color)
            self.tedit.append(self.edit4.text())

    def on_click_graph(self):
        self.graph.show()
    

    # Timer Loop to update Unit Serial and LTC Serial.
    def timerEvent(self, event):
        
        # Read String from Main Serial Port
        if self.flag:
            try:
                
                if self.ser.isOpen():
                    string = self.ser.readline()
                    if string != b'':
                        self.line = string.decode("utf-8", errors = 'replace')
                        
                        # update string to graph for retrieve
                        if self.graph.isVisible() and not self.LTC_ser.isOpen():
                            self.graph.updateStream(self.line, ltc_data = None)
                            
                        t = time.strftime ('[%H:%M:%S]:>', time.localtime ())
                        self.line = '>' + self.line[:-2]
                        self.tedit.append(self.line.replace('>', t))
                        self.tedit.moveCursor(QTextCursor.End)
#                         print(self.line)
            except Exception as e:
                    print(e)
                    
            # Read ADC data from Arduino Board.        
            if self.LTC_ser.isOpen():
                try:
                    # Set 'G' to get 30 bytes ADC data.
                    self.LTC_ser.write(b'G')
                    # Stop timer, in case ADC reading is out of timer loop.
                    self.timer.stop()
                    string = self.LTC_ser.readline()
                    if string != b'':
                        string = string.decode("utf-8", errors = 'replace')
                        
                        # Convert string stream to List, sort list from small to high
                        data_list = eval(string)

                        filted_data = kalmanfilter.KalmanFilter(data_list, n_iter= len(data_list))
                        self.filtering_data.append(filted_data[-1])
                        #sorted_list = sorted(data_list)
                        #print('data list=', tuple(filted_data), 'mean=', filted_data[-1])
                        with open('./log.csv', 'a+') as fl:
                            fl.write('Raw:,' + str(data_list))
                            fl.write('\n')
                            fl.write('Filtered:,' + str(tuple(filted_data)))
                            fl.write('\n')
                            fl.write('Tracking:,' + str(tuple(kalmanfilter.KalmanFilter(self.filtering_data, n_iter= len(self.filtering_data)))))
                            fl.write('\n')
                        # Get Compensation input
                        number = self.LTC_Comp_edit.text()
                        if number != '':
                           compensation = float(number)
                        else:
                            compensation = 0.0
                            
                        # Data from ADC can be variant, this step shall consider t remove noise
                        # 
                        median = filted_data[-1] + compensation
                        self.LTC_label.setText(str('%2.2f'%median))
                        
                        self.graph.updateStream(self.line, ltc_data = median)

                        # Write data to CSV file and save it.
                        if self.line != '':
                            t = time.strftime ('[%H:%M:%S],', time.localtime ())
                            text = self.line.replace('>', t + ',' + str('%2.2f'%median) + ',' )
                            if(self.file != ''):
                                with open(self.file, 'a+') as f:
                                        f.write(text)
                                        f.write('\n')
                                self.edit3.setText('Saving:'+ text)
                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, 'Warning', e)

                # take care to clean self.line each time before loop ends.
                self.line = ''                        
                self.timer.start(100, self)
            else:
                # Write data to CSV file and save it.
                if self.line != '':
                    t = time.strftime ('[%H:%M:%S],>', time.localtime ())
                    text = self.line.replace('>', t )
                    if(self.file != ''):
                        with open(self.file, 'a+') as f:
                                f.write(text)
                                f.write('\n')
                        self.edit3.setText('Saving:'+ text)                
                # take care to clean self.line each time before loop ends.
                self.line = ''

# Start to run application                    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
