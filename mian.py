
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
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication, QObject, QRunnable, QThreadPool




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
        self.I = QVBoxLayout(self.plot)
        self.I.addWidget(self.canvas)
        self.ax.set_title('TSP Problem')
        self.ax.patch.set_facecolor('wheat')



        self.numberOfCities = 0
        self.cities = []
        self.firstCityToVisit = "None"
        self.exhaustiveSearchRuntime = 'None'
        self.minimumXPoint = 'None'
        self.minimumYPoint = 'None'
        self.maximumXPoint = 'None'
        self.maximumYPoint = 'None'

        self.addFile.clicked.connect(self.addFileCalled)
        self.execute.clicked.connect(self.executeCalled)

    def executeCalled(self):
        if self.es.isChecked():
            self.exhaustiveSearch(self.cities)
        elif self.nn.isChecked():
            self.nearestNeighbourAlgorithm()
        else:
            print('Choose an algorithm!')

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
        self.timelabel.hide()
        self.distlabel.setText('Algorithm Finished Just Plotting...')
        redrawingThread = drawingThread(self.canvas)
        cnt = 0
        for point in perm:
            if cnt == len(perm) - 1:

                self.ax.set_ylim(self.minimumYPoint.y - 0.5, self.maximumYPoint.y + 0.5)
                self.ax.set_xlim(self.minimumXPoint.x - 0.5, self.maximumXPoint.x + 0.5)
                self.ax.plot([point.x, perm[0].x], [point.y, perm[0].y], 'bo-')
                self.ax.set_title('TSP Problem')
                self.ax.patch.set_facecolor('wheat')
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                time.sleep(1)

            else:

                self.ax.set_ylim(self.minimumYPoint.y - 0.5, self.maximumYPoint.y + 0.5)
                self.ax.set_xlim(self.minimumXPoint.x - 0.5, self.maximumXPoint.x + 0.5)
                self.ax.plot([point.x,perm[cnt + 1].x], [point.y,perm[cnt + 1].y], 'ro-')
                self.ax.set_title('TSP Problem')
                self.ax.patch.set_facecolor('wheat')
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                time.sleep(1)
            cnt = cnt + 1
        self.ax.set_title('TSP Problem')
        self.ax.patch.set_facecolor('wheat')

    def getNameOfNearestUnvisitedPoint(self, point, indexOfPoint):
        distanceToallOtherPoints = {}
        for city in self.cities:
            if self.cities.index(city) == indexOfPoint:
                continue
            else:
                if city.isVisited == False:
                    distanceToallOtherPoints[city.name] = self.distanceOfTwoPoint(city, point)
                else:
                    continue
        if distanceToallOtherPoints == {}:
            return 'end'
        else:
            key_min = min(distanceToallOtherPoints.keys(), key=(lambda k: distanceToallOtherPoints[k]))
            return int(key_min[1:]) - 1

    def nearestNeighbourAlgorithm(self):
        print('Nearest neighbour started...')
        for city in self.cities:
            city.isVisited = False
        t_start = time.clock()
        permutaionOfPoints = []
        totalDistance = 0
        self.cities[0].isVisited = True
        permutaionOfPoints.append(self.cities[0])
        indexOFCurrentCity = 0
        while self.getNameOfNearestUnvisitedPoint(self.cities[indexOFCurrentCity],indexOFCurrentCity) != 'end':
            IndexNextCity = self.getNameOfNearestUnvisitedPoint(self.cities[indexOFCurrentCity], indexOFCurrentCity)
            permutaionOfPoints.append(self.cities[IndexNextCity])
            totalDistance = totalDistance + self.distanceOfTwoPoint(self.cities[indexOFCurrentCity], self.cities[IndexNextCity])
            self.cities[IndexNextCity].isVisited = True
            indexOFCurrentCity = IndexNextCity
        totalDistance = totalDistance + self.distanceOfTwoPoint(self.cities[indexOFCurrentCity], self.cities[0])
        t_end = time.clock()
        delta = t_end - t_start
        print('------------------------------')
        print('Nearest neighbour algorithm:')
        print('Optimum Path:')
        for index in range(0, self.numberOfCities):
            print(permutaionOfPoints[index].name, end='-')
        print(': ', totalDistance)
        print('Runtime: ', delta)
        self.ax.clear()
        self.plotAGivenPermutation(permutaionOfPoints)
        self.canvas.draw()
        x = delta
        self.timelabel.show()
        self.timelabel.setText('Nearest neighbour Runtime = ' + '{:.4e}'.format(x) + 's')
        x = totalDistance
        self.distlabel.setText('Nearest neighbour Distance = ' + '{:.4f}'.format(x) + 'Km')

    def exhaustiveSearch(self, set):
        for city in self.cities:
            city.isVisited = False
        print('Exhaustive search started...')
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
        print('Exhaustive Search:')
        print('Optimum Path:')
        for index in range(0,self.numberOfCities):
            print(allPossiblePermutations[IndexOfMinimimDistanceAmongPermutations][index].name,end = '-')
        print(': ', minimumDistanceAmongPermutations)
        print('Runtime: ', self.exhaustiveSearchRuntime)

        listOfBestPermutation = list(allPossiblePermutations[IndexOfMinimimDistanceAmongPermutations])
        self.ax.clear()
        self.plotAGivenPermutation(listOfBestPermutation)
        x = self.exhaustiveSearchRuntime
        self.timelabel.show()
        self.timelabel.setText('Exhaustive seacrh Runtime = ' + '{:.4e}'.format(x) + 's')
        x = minimumDistanceAmongPermutations
        self.distlabel.setText('Exhaustive seacrh Distance = ' + '{:.4}'.format(x) + 'Km')



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
                self.cities.clear()
                for element in linesOfFile:
                    if counter == 0:
                        self.numberOfCities = int(element)
                    else:
                        splitedElement = element.split(' ')
                        self.cities.append(Point(float(splitedElement[0]),float(splitedElement[1]), False, 'P'+str(counter)))
                    counter = counter + 1

                self.firstCityToVisit = self.cities[0]
                self.minimumXPoint = min(self.cities, key=(lambda k: k.x))
                self.minimumYPoint = min(self.cities, key=(lambda k: k.y))
                self.maximumXPoint = max(self.cities, key=(lambda k: k.x))
                self.maximumYPoint = max(self.cities, key=(lambda k: k.y))
                self.ax.set_ylim(self.minimumYPoint.y - 0.5, self.maximumYPoint.y + 0.5)
                self.ax.set_xlim(self.minimumXPoint.x - 0.5, self.maximumXPoint.x + 0.5)
                self.canvas.draw()




class drawingThread(QThread):
    def __init__(self, canvas):
        self.canv = canvas
    def run(self):
        self.canv.draw()
app = QApplication(sys.argv)
w = intro()
w.resize(1400,900)
w.setWindowTitle("TSP Problem")
w.show()
sys.exit(app.exec())
