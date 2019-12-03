#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
from TSPState import TSPState
import heapq
import itertools
from heapq import heappop, heappush
from copy import deepcopy



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	def greedy( self,time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		startIndex = 0
		startCity = cities[startIndex]
		currentCity = startCity
		route = []
		while not foundTour and time.time()-start_time < time_allowance and startIndex < len(cities) - 1:
			next = None

			for city in cities:
				if city != currentCity and city not in route:
					if next == None and currentCity.costTo(city) != np.inf:
						next = city
					elif next != None:
						if currentCity.costTo(city) < currentCity.costTo(next):
							next = city

			if next == None:
				startIndex += 1
				currentCity = cities[startIndex]
				route = []
			else:
				route.append(next)
				currentCity = next
				if len(route) == ncities:
					bssf = TSPSolution(route)
					count += 1
					if bssf.cost < np.inf:
						# Found a valid route
						foundTour = True
					else:
						startIndex += 1
						currentCity = cities[startIndex]
						route = []
			
		end_time = time.time()
		self.greedyRoute = route
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results
	
	
	
	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''
		
	def branchAndBound( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		startIndex = 0
		startCity = cities[startIndex]
		currentCity = startCity
		self.greedy()
		route = self.greedyRoute
		bssf = TSPSolution(route)
		foundTour = True
		heap = []
		iState = TSPState([cities[0]], cities, 0)
		iState.initMatrix()
		iState.reduceMatrix()
		heappush(heap, iState)
		start_time = time.time()
		maxHeapSize = 1
		totalStates = 1
		prunedStates = 0
		while (time.time()-start_time) < time_allowance and len(heap) > 0:
		# while len(heap) > 0:
			if len(heap) > maxHeapSize:
				maxHeapSize = len(heap)

			print(len(heap), " items remaining in heap")
			currentState = heappop(heap)
			if currentState.bestCost < bssf.cost:
				if len(currentState.path) == len(cities):
					# if currentState.bestCost < bssf.cost:
					lastCost = currentState.path[-1].costTo(currentState.path[0])
					currentState.bestCost += lastCost
					if currentState.bestCost < bssf.cost:
						bssf = TSPSolution(currentState.path)
				else:
					for city in cities:
						totalStates += 1
						if not currentState.inPath(city):
							newPath = deepcopy(currentState.path)
							newPath.append(city)
							newState = TSPState(newPath, cities, deepcopy(currentState.bestCost))
							newState.costMatrix = deepcopy(currentState.costMatrix)
							newState.coveredCols = deepcopy(currentState.coveredCols)
							newState.coveredRows = deepcopy(currentState.coveredRows)
							city1 = newState.path[newState.len() - 2]
							city2 = newState.path[newState.len() - 1]
							newState.coverCities(city1._index, city2._index)
							newState.reduceMatrix()
							if newState.bestCost < bssf.cost:
								heappush(heap, newState)
							else:
								prunedStates += 1
						else:
							prunedStates += 1
			else:
				prunedStates += 1
		# 	next = None

		# 	for city in cities:
		# 		if city != currentCity and city not in route:
		# 			if next == None and currentCity.costTo(city) != np.inf:
		# 				next = city
		# 			elif next != None:
		# 				if currentCity.costTo(city) < currentCity.costTo(next):
		# 					next = city

		# 	if next == None:
		# 		startIndex += 1
		# 		currentCity = cities[startIndex]
		# 		route = []
		# 	else:
		# 		route.append(next)
		# 		currentCity = next
		# 		if len(route) == ncities:
		# 			bssf = TSPSolution(route)
		# 			count += 1
		# 			if bssf.cost < np.inf:
		# 				# Found a valid route
		# 				foundTour = True
		# 			else:
		# 				startIndex += 1
		# 				currentCity = cities[startIndex]
		# 				route = []
			
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = maxHeapSize
		results['total'] = totalStates
		results['pruned'] = prunedStates
		return results



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
		
	def fancy( self,time_allowance=60.0 ):
		pass
		



