# coding = utf-8

# Develop by: Daniel G.
# Date: 2019-07-02

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Graph(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Graph Plotting')
        self.setWindowIcon(QIcon(r'./sweep data.ico'))
        self.initGui()
    
    def initGui(self):
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Setup a label widget to show temperature in Fahrenheit
#         self.label_temp = QLabel(self)
# 
#         self.label_temp.setFont(QFont("Microsoft YaHei",18,QFont.Bold))
#         self.label_temp.setAlignment(Qt.AlignCenter)
#         self.label_temp.setText('Temperature reading: 0.0*F 0.0*C')

        # to include canvas related widgets
        h1 = QVBoxLayout()
        h1.addWidget(self.toolbar)
#         h1.addWidget(self.label_temp)
        h1.addWidget(self.canvas)
        
        h2 = QHBoxLayout()
        h3 = QVBoxLayout()
        self.content_label = QLabel()
        self.content_label.setText('Add a Name to Plot')
        h3.addWidget(self.content_label)
        
        self.cnt_text = QLineEdit()
        h3.addWidget(self.cnt_text)
        
        self.list = QListWidget()
        h3.addWidget(self.list) 
        
        h2.addLayout(h3)
        
        h4 = QVBoxLayout()
        self.addBtn = QPushButton()
        self.addBtn.setText('Add')
        self.addBtn.clicked.connect(self.on_click_add) 
        h4.addWidget(self.addBtn)
        
        self.clearBtn = QPushButton()
        self.clearBtn.setText('Clear')
        self.clearBtn.clicked.connect(self.on_click_clear) 
        h4.addWidget(self.clearBtn)
        
        self.plotBtn = QPushButton()
        self.plotBtn.setText('Begin Plotting')
        self.plotBtn.clicked.connect(self.on_click_plot)
        
        h4.addWidget(self.plotBtn)

        self.stopBtn = QPushButton()
        self.stopBtn.setText('Stop Plotting')
        self.stopBtn.clicked.connect(self.on_click_stop)
        self.stopBtn.setEnabled(False)
        
        h4.addWidget(self.stopBtn)
                
        h2.addLayout(h4)   
             
        h1.addLayout(h2) 
        
        self.setLayout(h1)
        
        # Canvas settings
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True)
        
        self.ax.set_ylabel('Counts')
        self.ax.set_xlabel('LTC sensitivity/uA')
        
        self.dict = dict()
        
        self.itemsTextList = list()
        
        self.x_data = list()
        
        self.flag = False
        
        
        # Define timer to loop events
        self.timer = QBasicTimer()
#         self.timer.start(300, self)
    
    
    def on_click_add(self):
        try:
            self.list.addItems([self.cnt_text.text()])
            self.itemsTextList =  [str(self.list.item(i).text()) for i in range(self.list.count())]
#             print(self.itemsTextList)
            for item in self.itemsTextList:
#                 print(item)
                self.dict.update({item:[]})
#             print(self.dict)
        except Exception as e:
            print(e)
    
    def on_click_clear(self):
        self.flag = False
        self.timer.stop()
        
        self.list.clear()
        self.x_data = []
        self.dict.clear()
        
        self.plotBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)    
    
    def on_click_plot(self):
        self.flag = True
        self.timer.start(400, self)
        self.plotBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)
    
        
    def on_click_stop(self):
        self.flag = False
        self.timer.stop()
#         self.x_data = []
#         for key in self.dict:
#             self.dict[key] = []
            
        self.plotBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
            
    def updateStream(self, str, ltc_data = None):
#         print('in class Graph:')
        var1 = str.replace('\r', '')
        trimedString = var1.split('>')
        
        if len(self.itemsTextList) !=0:
            for item in self.itemsTextList:
                for seg in trimedString:
                    if (item + ':') in seg:
    #                     print(seg, seg.split(':')[1])
                        self.dict[item].append(int(seg.split(':')[1]))
    #                     print(self.dict)
            if ltc_data is not None:
                self.x_data.append(ltc_data)
            else:
                self.x_data = []
    #         print('end printing....')
    #         print(self.x_data, str, self.dict)
        
    def update_plotting(self):
    
        # discards the old graph
        try:
            if bool(self.dict):
                self.ax.cla()
                self.ax.grid(True)
                
                for key in self.dict:
                    if len(self.x_data) == 0:
                        self.ax.plot(self.dict[key], label = str(key))
                    else:
#                         print(self.x_data, self.dict[key])
                        self.ax.plot(self.x_data, self.dict[key], label = str(key))
               
                self.ax.legend(loc = 'upper left')
     
                self.ax.set_ylabel('Counts')
                if len(self.x_data) == 0:
                    self.ax.set_xlabel('Data numbers')
                else:
                    self.ax.set_xlabel('Smoke sensitivity(uA)')
     
                # refresh canvas
                self.canvas.draw()
                
        except Exception as e:
            print(e)      
                # to show legend()

        
    def timerEvent(self, event):
        if self.flag:
#             print('plotting....')
            self.update_plotting()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Graph()
    ex.show()
    sys.exit(app.exec_())