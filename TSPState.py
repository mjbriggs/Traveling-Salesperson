import numpy as np
from TSPClasses import *
import itertools

class TSPState:
    def __init__(self, path, cities, bestCost):
        super().__init__()
        self.bestCost = bestCost
        self.path = path
        self.cities = cities
    """
        comparison function used by the heapq library. Initially compares the path length, choosing the longer path. 
        If the paths are the same length, then the current cost is used to compare heap values
        O(1) 
    """
    def __lt__(self, value):
        if len(self.path) is not len(value.path):
            return len(self.path) > len(value.path)
        else:
            return self.bestCost < value.bestCost
    
    """         
        Initializes cost matrix to the costs between cities.
        O(n^2)
    """    
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

    """
        Grabs the travel cost from one city to the other. The from row, the to column, and the value at (toCity, fromCity) 
        are set to infinity. If cost is infinity, this operation is skipped because we are throwing out this state anyways
        O(2n + 1)
    """
    def coverCities(self, fromCity, toCity):
        self.bestCost += self.costMatrix[fromCity][toCity]
        if self.bestCost != np.inf:
            self.infRow(fromCity)
            self.infCol(toCity)
            self.infPair(fromCity, toCity)

    """
        Performs row and column reduction operations on the cost matrix. If best cost is infinity, this operation is skipped because 
        the best cost will still be infinity, meaning the state will never enter the queue anyways
        O(kn^2) # where k is the number of cities
    """
    def reduceMatrix(self):
        if self.bestCost != np.inf:
            self.reduceMatrixRows()
            self.reduceMatrixCols()
    """
        Performs a row reduction on every row by subtracting the minimum row value from every value in the row. This function also increments the bestCost 
        value. Operation is skipped if min value is 0 or infinity, due to the redundancy of such an operation. 
        O(kn + k) #  where k is the number of cities
    """
    def reduceMatrixRows(self):
        for row in range(len(self.costMatrix)):
            min, minIndex = self.findRowMin(row)
            if min != np.inf and min > 0:
                self.reduceRow(row, min, minIndex)
                self.bestCost += min
    """
        Performs a col reduction by subtracting the minimum col value from every value in the col. This function also increments the bestCost 
        value. Operation is skipped if min value is 0 or infinity, due to the redundancy of such an operation. 
        O(kn + k) #  where k is the number of cities
    """
    def reduceMatrixCols(self):
        for col in range(len(self.costMatrix[0])):
            min, minIndex = self.findColMin(col)
            if min != np.inf and min > 0:
                self.reduceCol(col, min, minIndex)
                self.bestCost += min
    """
        This function actually performs the row reduction, subtracting the min value from the row
        O(n)
    """
    def reduceRow(self, row, min, minIndex):
        for col in range(len(self.costMatrix[row])):
            newCost = self.costMatrix[row][col] - min
            if newCost == np.nan:
                self.costMatrix[row][col] = np.inf
            else:
                self.costMatrix[row, col] = newCost
    """
        This function actually performs the column reduction, subtracting the min vale from the column
        O(n)
    """
    def reduceCol(self, col, min, minIndex):
        for row in range(len(self.costMatrix)):
            newCost = self.costMatrix[row][col] - min
            if newCost == np.nan:
                self.costMatrix[row][col] = np.inf
            else:
                self.costMatrix[row, col] = newCost
    """
        Iterates through a row to find a minimum value and it's location
        O(n)
    """
    def findRowMin(self, row):
        min = self.costMatrix[row][0]
        minIndex = 0
        for col in range(len(self.costMatrix[row])):
            if self.costMatrix[row][col] < min:
                min = self.costMatrix[row][col]
                minIndex = col
        
        return min, minIndex
    """
        Iterates through a column to find a minimum value and it's location
        O(n)
    """
    def findColMin(self, col):
        min = self.costMatrix[0][col]
        minIndex = 0
        row = 0
        for row in range(len(self.costMatrix)):
            if self.costMatrix[row][col] < min:
                min = self.costMatrix[row][col]
                minIndex = row
        return min, minIndex

    """
        Iterates through a row and sets each value to infinity
        O(n)
    """
    def infRow(self, row):
        for i in range(len(self.costMatrix[row])):
            self.costMatrix[row][i] = np.inf
    """
        Iterates through a column and sets each value to infinity
        O(n)
    """
    def infCol(self, col):
        for i in range(len(self.costMatrix)):
            self.costMatrix[i][col] = np.inf
    """
        Sets the cost from the column city to the row city to infinity
        O(1)
    """
    def infPair(self, row, col):
        self.costMatrix[col][row] = np.inf
        
    