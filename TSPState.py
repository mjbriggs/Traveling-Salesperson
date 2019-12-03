import numpy as np
from TSPClasses import *
import itertools

class TSPState:
    def __init__(self, path, cities, bestCost):
        super().__init__()
        self.bestCost = bestCost
        self.path = path
        self.cities = cities
        self.coveredCols = []
        self.coveredRows = []
    
    def __lt__(self, value):
        if len(self.path) is not len(value.path):
            return len(self.path) > len(value.path)
        else:
            return self.bestCost < value.bestCost
    
    def initMatrix(self):
        self.costMatrix = np.zeros(shape=(len(self.cities), len(self.cities)))
        row_index = 0
        col_index = 0
        for fromCity in self.cities:
            col_index = 0
            for toCity in self.cities:
                self.costMatrix[row_index][col_index] = fromCity.costTo(toCity)
                col_index += 1
            row_index += 1
    
    def __str__(self):
        return str(self.costMatrix)
    
    def len(self):
        return len(self.path)
    
    def inPath(self, city):
        for val in self.path:
            if val._index == city._index:
                return True
        return False
    
    def setMatrix(self, matrix):
        self.costMatrix = matrix

    def coverCities(self, fromCity, toCity):
        self.bestCost += self.costMatrix[fromCity][toCity]
        if self.bestCost != np.inf:
            self.infRow(fromCity)
            self.infCol(toCity)
            self.infPair(fromCity, toCity)

    def reduceMatrix(self):
        if self.bestCost != np.inf:
            self.reduceMatrixRows()
            self.reduceMatrixCols()
    
    def reduceMatrixRows(self):
        for row in range(len(self.costMatrix)):
            min, minIndex = self.findRowMin(row)
            if min != np.inf and min > 0:
                self.reduceRow(row, min, minIndex)
                self.bestCost += min
    
    def reduceMatrixCols(self):
        for col in range(len(self.costMatrix[0])):
            min, minIndex = self.findColMin(col)
            if min != np.inf and min > 0:
                self.reduceCol(col, min, minIndex)
                self.bestCost += min
        
    def reduceRow(self, row, min, minIndex):
        for col in range(len(self.costMatrix[row])):
            # if col != minIndex:
            newCost = self.costMatrix[row][col] - min
            if newCost == np.nan:
                self.costMatrix[row][col] = np.inf
            else:
                self.costMatrix[row, col] = newCost
    
    def reduceCol(self, col, min, minIndex):
        for row in range(len(self.costMatrix)):
            # if row != minIndex:
            newCost = self.costMatrix[row][col] - min
            if newCost == np.nan:
                self.costMatrix[row][col] = np.inf
            else:
                self.costMatrix[row, col] = newCost

    def findRowMin(self, row):
        min = self.costMatrix[row][0]
        minIndex = 0
        for col in range(len(self.costMatrix[row])):
            if self.costMatrix[row][col] < min:
                min = self.costMatrix[row][col]
                minIndex = col
        
        return min, minIndex

    def findColMin(self, col):
        min = self.costMatrix[0][col]
        minIndex = 0
        row = 0
        for row in range(len(self.costMatrix)):
            if self.costMatrix[row][col] < min:
                min = self.costMatrix[row][col]
                minIndex = row
        return min, minIndex

    def infRow(self, row):
        for i in range(len(self.costMatrix[row])):
            self.costMatrix[row][i] = np.inf
        self.coveredRows.append(row)

    def infCol(self, col):
        for i in range(len(self.costMatrix)):
            self.costMatrix[i][col] = np.inf
        self.coveredCols.append(col)
    
    def infPair(self, row, col):
        self.costMatrix[col][row] = np.inf
        
    