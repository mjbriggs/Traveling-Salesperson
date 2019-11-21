import numpy as np
from TSPClasses import *
import itertools

class TSPState:
    def __init__(self, path, cities, bestCost):
        super().__init__()
        self.bestCost = bestCost
        self.path = path
        self.cities = cities
    
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
        for row in range(len(self.costMatrix)):
            min, minIndex = self.findRowMin(row)
            self.reduceRow(row, min, minIndex)
            self.bestCost += min
        
    def reduceRow(self, row, min, minIndex):
        for col in range(len(self.costMatrix[row])):
            if col != minIndex:
                newCost = self.costMatrix[row][col] - min
                self.costMatrix[row][col] = newCost

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
        row = 0
        for row in range(len(self.costMatrix)):
            if self.costMatrix[row][col] < min:
                min = self.costMatrix[row][col]
                minIndex = row
        
    