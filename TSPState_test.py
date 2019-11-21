import unittest
from TSPClasses import *
from TSPState import *
from Proj5GUI import *
from copy import deepcopy

class TestTSPState(unittest.TestCase):

    def setUp(self):
        app = QApplication(sys.argv)
        proj5Gui = Proj5GUI("test")
        SCALE = 1.0
        proj5Gui.curSeed = QLineEdit("10")
        proj5Gui.data_range = { 'x':[-1.5*SCALE,1.5*SCALE], \
								'y':[-SCALE,SCALE] }
        proj5Gui.size = QLineEdit("10")
        self.testScenario = Scenario(proj5Gui.newPoints(), "Hard (Deterministic)", 20)
        self.testState = TSPState(self.testScenario.getCities(), self.testScenario.getCities(), 0)
        self.testState.initMatrix()
        print(self.testState.costMatrix)

    def test_init(self):
        self.assertEqual(1,1)
        state = TSPState(self.testScenario.getCities(), self.testScenario.getCities(), 0)
        self.assertEqual(state.path, self.testScenario.getCities())
        self.assertEqual(state.cities, self.testScenario.getCities())
        state.initMatrix()

        row_index = 0
        col_index = 0
        for fromCity in self.testScenario.getCities():
            col_index = 0
            for toCity in self.testScenario.getCities():
                self.assertEqual(state.costMatrix[row_index][col_index], fromCity.costTo(toCity))
                col_index += 1
            row_index += 1
    
    def test_find_row_min(self):
        min, minIndex = self.testState.findRowMin(2)
        self.assertEqual(min, 246)
        self.assertEqual(minIndex, 9)
    
    def test_reduce_row(self):
        oldRow = deepcopy(self.testState.costMatrix[2])
        print(self.testState.costMatrix[2])
        self.testState.reduceRow(2, 246, 9)

        print(self.testState.costMatrix[2])
        for col_index in range(len(self.testState.costMatrix[2])):
            if col_index != 9:
                self.assertEqual(self.testState.costMatrix[2][col_index], oldRow[col_index] - 246)
            else:
                self.assertEqual(self.testState.costMatrix[2][col_index], oldRow[col_index])
    
    def test_reduce_0_row(self):
        oldRow = deepcopy(self.testState.costMatrix[0])
        print(self.testState.costMatrix[0])
        self.testState.reduceRow(0, 0, 4)

        print(self.testState.costMatrix[0])
        for col_index in range(len(self.testState.costMatrix[0])):
            self.assertEqual(self.testState.costMatrix[0][col_index], oldRow[col_index])
    
    def test_reduce_matrix(self):
        oldMatrix = deepcopy(self.testState.costMatrix)
        rowMins = []
        newBest = 0
        for row in range(len(self.testState.costMatrix)):
            min, minIndex = self.testState.findRowMin(row)
            minVal = {'min': min, 
                'minIndex': minIndex}
            rowMins.append(minVal)
            newBest += min
        
        self.testState.reduceMatrix()

        for row_index in range(len(self.testState.costMatrix)):
            for col_index in range(len(self.testState.costMatrix[row_index])):
                if col_index != rowMins[row_index]['minIndex']:
                    self.assertEqual(self.testState.costMatrix[row_index][col_index],
                    oldMatrix[row_index][col_index] - rowMins[row_index]['min'])
        self.assertEqual(newBest, self.testState.bestCost)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestTSPState())
    return suite

if __name__ == '__main__':
    print("in main test method")
    runner = unittest.TextTestRunner()
    runner.run(suite())
