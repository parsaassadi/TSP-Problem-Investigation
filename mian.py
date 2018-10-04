
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
import time




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
        self.exhaustiveSearchRuntime = 'None'

        self.addFile.clicked.connect(self.addFileCalled)
        self.execute.clicked.connect(self.executeCalled)

    def executeCalled(self):
        if self.es.isChecked():
            self.exhaustiveSearch(self.cities)
        elif self.nn.isChecked():
            print('linear')
        else:
            print('Choose an alg!')

    def distanceOfTwoPoint(self, point1, point2):
        return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def cummulativeSumOfDistancesOfPermutation(self, perms):
        differentDistancesMadeByEachPermutation = []
        currentSum = 0
        counter = 0
        for permutation in list(perms):
            for element in permutation:
                if counter == len(permutation) - 1:
                    currentSum = currentSum + self.distanceOfTwoPoint(element, permutation[0])
                else:
                    currentSum = currentSum + self.distanceOfTwoPoint(element, permutation[counter + 1])
                    counter = counter + 1
            differentDistancesMadeByEachPermutation.append(currentSum)
            currentSum = 0
            counter = 0
        return differentDistancesMadeByEachPermutation

    def plotAGivenPermutation(self, perm):
        cnt = 0
        for point in perm:
            if cnt == len(perm) - 1:
                self.ax.plot([point.x, perm[0].x], [point.y, perm[0].y], 'bo-')
            else:
                self.ax.plot([point.x,perm[cnt + 1].x], [point.y,perm[cnt + 1].y], 'ro-')
            cnt = cnt + 1

        self.canvas.draw()

    def exhaustiveSearch(self, set):
        print('Exhaustive Search:')
        t_start = time.clock()
        allPermutations = permutations(set,len(set))
        allPossiblePermutations = []
        for permutation in list(allPermutations):
            if permutation[0].name == 'P1':
                allPossiblePermutations.append(permutation)
            else:
                continue

        minimumDistanceAmongPermutations = min(self.cummulativeSumOfDistancesOfPermutation(allPossiblePermutations))
        IndexOfMinimimDistanceAmongPermutations = self.cummulativeSumOfDistancesOfPermutation(allPossiblePermutations)\
            .index(minimumDistanceAmongPermutations)
        t_end = time.clock()
        self.exhaustiveSearchRuntime = t_end - t_start

        #############################################################
        ### UNCOMMMENT THESE LINES FOR DISPLAYNG ALL PERMUTATIONS ###
        #############################################################
        #cnt = 0
        #for permutation in list(allPossiblePermutations):
        #    for element in permutation:
        #        print(element.name,end ='-')
        #    print(': ',self.cummulativeSumOfDistancesOfPermutation(allPossiblePermutations)[cnt])
        #    cnt = cnt + 1

        print('------------------------------')
        print('Optimum Path:')
        for index in range(0,self.numberOfCities):
            print(allPossiblePermutations[IndexOfMinimimDistanceAmongPermutations][index].name,end = '-')
        print(': ', minimumDistanceAmongPermutations)
        print('Runtime: ', self.exhaustiveSearchRuntime)

        listOfBestPermutation = list(allPossiblePermutations[IndexOfMinimimDistanceAmongPermutations])
        self.plotAGivenPermutation(listOfBestPermutation)








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

                self.firstCityToVisit = self.cities[0]

        self.exhaustiveSearch(self.cities)




app = QApplication(sys.argv)
w = intro()
w.resize(1400,900)
w.setWindowTitle("TSP Problem")
w.show()
sys.exit(app.exec())
