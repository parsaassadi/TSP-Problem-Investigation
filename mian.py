
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLayout, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5 import uic
import os
import matplotlib
matplotlib.use("QT5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as f
from matplotlib.figure import Figure
import numpy as np


class Point:
    def __init__(self, X, Y, visited):
        self.x = X
        self.y = Y
        self.isVisited = visited

form = uic.loadUiType(os.path.join(os.getcwd(),"TSPUi.ui"))[0]
class intro(form, QMainWindow):
    def __init__(self):
        form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.fig = Figure()
        self.ax = self.fig.add_axes([0.1,0.1,0.8,0.8])
        self.canvas = f(self.fig)
        I = QVBoxLayout(self.plot)
        I.addWidget(self.canvas)

        self.numberOfCities = 0
        self.cities = []

        self.addFile.clicked.connect(self.addFileCalled)

    def distanceOfTwoPoint(self, point1, point2):
        return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


    def addFileCalled(self):
        f = QFileDialog.getOpenFileName(self)
        if f[0] == '':
            print("Directory Not chosen!")
        else:
            with open(f[0], 'r') as iFile:
                fileAsString = iFile.read()
                linesOfFile = iFile.readlines()
                linesOfFile = [line.rstrip('\n') for line in open(f[0])]
                counter = 0
                for element in linesOfFile:
                    if counter == 0:
                        self.numberOfCities = int(element)
                    else:
                        self.cities.append(Point(float(element[0]),float(element[2]), False))
                    counter = counter + 1
                print('Contents Of File:')
                print(self.numberOfCities)
                for element in self.cities:
                    print(element.x, element.y)







app = QApplication(sys.argv)
w = intro()
w.resize(1400,900)
w.setWindowTitle("TSP Problem")
w.show()
sys.exit(app.exec())
