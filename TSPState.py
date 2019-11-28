import numpy as np
from TSPClasses import *
import itertools

class TSPState:
    def __init__(self, path, cities, bestCost):
        super().__init__()
        self.bestCost = bestCost
        self.path = path
        self.cities = cities
    
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
    
    def setMatrix(self, matrix):
        self.costMatrix = matrix

    def reduceMatrix(self):
        self.reduceMatrixRows()
        self.reduceMatrixCols()
    
    def reduceMatrixRows(self):
        for row in range(len(self.costMatrix)):
            min, minIndex = self.findRowMin(row)
            if min is not np.inf and min is not 0:
                self.reduceRow(row, min, minIndex)
                self.bestCost += min
    
    def reduceMatrixCols(self):
        for col in range(len(self.costMatrix[0])):
            min, minIndex = self.findColMin(col)
            if min is not np.inf and min is not 0:
                self.reduceCol(col, min, minIndex)
                self.bestCost += min
        
    def reduceRow(self, row, min, minIndex):
        for col in range(len(self.costMatrix[row])):
            if col != minIndex:
                newCost = self.costMatrix[row][col] - min
                self.costMatrix[row, col] = newCost
    
    def reduceCol(self, col, min, minIndex):
        for row in range(len(self.costMatrix)):
            if row != minIndex:
                newCost = self.costMatrix[row][col] - min
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
        
    