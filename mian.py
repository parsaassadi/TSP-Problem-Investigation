
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLayout, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5 import uic
import os
import matplotlib
matplotlib.use("QT5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as f
from matplotlib.figure import Figure
import numpy as np
from itertools import permutations




class Point:
    def __init__(self, X, Y, visited, nme):
        self.x = X
        self.y = Y
        self.isVisited = visited
        self.name = nme

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
        self.firstCityToVisit = "None"

        self.addFile.clicked.connect(self.addFileCalled)

    def distanceOfTwoPoint(self, point1, point2):
        return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def cummulativeSumOfDistancesOfPermutation(self, perms):
        differentDistancesMadeByEachPermutation = []
        currentSum = 0
        counter = 0
        for permutation in list(perms):
            for element in permutation:
                if counter == len(permutation) - 1:
                    break
                else:
                    currentSum = currentSum + self.distanceOfTwoPoint(element, permutation[counter + 1])
                    counter = counter + 1
            differentDistancesMadeByEachPermutation.append(currentSum)
            currentSum = 0
            counter = 0
        return differentDistancesMadeByEachPermutation


    def exhaustiveSearch(self, set):
        allPermutations = permutations(set,len(set))
        allPossiblePermutations = []
        for permutation in list(allPermutations):
            if permutation[0].name == 'P1':
                allPossiblePermutations.append(permutation)
            else:
                continue


        for permutation in list(allPossiblePermutations):
            for element in permutation:
                print(element.name)
            print('-------------')
        print(self.cummulativeSumOfDistancesOfPermutation(allPossiblePermutations))




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
                        splitedElement = element.split(' ')
                        self.cities.append(Point(float(splitedElement[0]),float(splitedElement[1]), False, 'P'+str(counter)))
                    counter = counter + 1
                print('Contents Of File:')
                print(self.numberOfCities)
                for element in self.cities:
                    print(element.x, element.y)
                self.firstCityToVisit = self.cities[0]
                self.exhaustiveSearch(self.cities)




app = QApplication(sys.argv)
w = intro()
w.resize(1400,900)
w.setWindowTitle("TSP Problem")
w.show()
sys.exit(app.exec())
