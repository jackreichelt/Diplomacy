from enum import Enum
import re
import unittest

class Type(Enum):
	land = 0
	sea = 1
	supply = 2
	army = 0
	fleet = 1

	def stringToInt(givenType):
		if givenType.lower() == 'land' or givenType.lower() == 'army' or\
			givenType.lower() == 'a':
			return 0
		elif givenType.lower() == 'sea' or givenType.lower() == 'fleet' or\
			givenType.lower() == 'f':
			return 1
		elif givenType.lower() == 'supply':
			return 2
		else:
			return -1

	def intToString(givenType, unit=False):
		if unit == False:
			if givenType == 0:
				return 'land'
			elif givenType == 1:
				return 'sea'
			else:
				return 'supply'
		else:
			if givenType == 0:
				return 'army'
			else:
				return 'fleet'

class Faction(Enum):
	england = 0
	france = 1
	germany = 2
	russia = 3
	ottoman = 4
	austria = 5
	italy = 6
	neutral = 7

	def stringToInt(faction):
		if faction.lower() == 'neutral':
			return 7
		elif faction.lower() == 'england':
			return 0
		elif faction.lower() == 'france':
			return 1
		elif faction.lower() == 'germany':
			return 2
		elif faction.lower() == 'russia':
			return 3
		elif faction.lower() == 'ottoman':
			return 4
		elif faction.lower() == 'austria':
			return 5
		elif faction.lower() == 'italy':
			return 6
		else:
			return -1

	def intToString(faction):
		if faction == 7:
			return 'neutral'
		elif faction == 0:
			return 'England'
		elif faction == 1:
			return 'France'
		elif faction == 2:
			return 'Germany'
		elif faction == 3:
			return 'Russia'
		elif faction == 4:
			return 'Ottoman'
		elif faction == 5:
			return 'Austria'
		elif faction == 6:
			return 'Italy'
		else:
			return 'error'

class Region(object):

	def __init__(self, name, abbrev, myType,
				owner = Faction.neutral):
		self.name = name
		self.abbrev = abbrev
		self.myType = myType
		self.owner = owner
		self.neighbours = []
		self.unit = None
		self.defensiveStrength = 0

	def __str__(self):
		return self.name

	def addNeighbour(self, neighbour):
		self.neighbours.append(neighbour)

	def changeOwner(self, newOwner):
		self.owner = newOwner

	def spawnUnit(self, unitType):
		newUnit = Unit(unitType, self)


class Unit(object):

	def __init__(self, unitType, location, owner):
		self.unitType = unitType
		self.location = location
		self.owner = owner
		self.ordered = False

class Order(object):
	unit = None
	location = None
	strength = 0

	def __init__(self, unit, location):
		self.unit = unit
		self.location = location
		self.strength = 1

		self.unit.ordered = True

class MoveOrder(Order):
	target = None

	def __init__(self, unit, location, target):
		self.unit = unit
		self.location = location
		self.strength = 1
		self.target = target

		self.unit.ordered = True

	def resolve(self):
		if self.strength > self.target.defensiveStrength:
			self.unit.location = self.target
			self.target.owner = self.location.owner
			#TODO: Mark unit in target location for retreat.

class Game(object):
	regions = []
	units = []
	orders = []
	futureOrders = []
	regionDict = {}

	def __init__(self):
		self.readRegions('regions.dat')
		self.connectAllRegions('neighbours.dat')
		self.readUnits('units.dat')

	def readRegions(self, filename):
		f = open(filename)
		print('reading regions')
		for line in f:
			parts = line.strip().split('\t')
			newRegion = Region(parts[0], parts[1], Type.stringToInt(parts[2]),
				Faction.stringToInt(parts[3]))
			self.regions.append(newRegion)

			# Set both the full name and the abbreviation to point to the new region
			self.regionDict[parts[0].lower()] = newRegion
			self.regionDict[parts[1].lower()] = newRegion
		f.close()
		print('regions read')

	def readUnits(self, filename):
		f = open(filename)
		print('reading units')
		for line in f:
			parts = line.strip().split('\t')

			if parts[1] in self.regionDict.keys():
				newUnit = Unit(Type.stringToInt(parts[0]), parts[1], Faction.stringToInt(parts[2]))

				self.regionDict[parts[1]].unit = newUnit

				self.units.append(newUnit)
		f.close()
		print('units read')

	def addOrder(self, order):
		holdOrder = re.compile('^([af]|fleet|army) (...+)[ -](holds?)')
		moveOrder = re.compile('^([af]|fleet|army) (...+)[ -](...+)$')
		supportOrder = re.compile('^([af]|fleet|army) (...) s (...*)$')
		convoyOrder = re.compile('^([af]|fleet|army) (...+) c (...*)$')

		moveMatch = moveOrder.match(order.lower())
		supportMatch = supportOrder.match(order.lower())
		convoyMatch = convoyOrder.match(order.lower())
		holdMatch = holdOrder.match(order.lower())

		# If we have found a move order
		if supportMatch != None or convoyMatch != None:
			futureOrders.append(order)

		elif moveMatch != None and holdMatch == None and supportMatch == None and convoyMatch == None:
			origin = moveMatch.group(2)
			target = moveMatch.group(3)

			if origin.unit == None or origin.unit.Type != Type.stringToInt(moveMatch.group(1)):
				# Invalid Order if there is no unit at the origin, or if the type doesn't match.
				return -1
			unit = origin.unit

			newOrder = MoveOrder(unit, origin, target)

			orders.append(newOrder)

	def findOrder(self, unit, location, target):
		for order in orders:
			if order.unit == unit and order.location == location and order.target == target:
				return order 

	def futureOrders(self):
		holdOrder = re.compile('^([af]|fleet|army) (...+)[ -](holds?)')
		moveOrder = re.compile('^([af]|fleet|army) (...+)[ -](...+)$')
		supportOrder = re.compile('^([af]|fleet|army) (...) s (...*)$')
		convoyOrder = re.compile('^([af]|fleet|army) (...+) c (...*)$')

		for order in futureOrders:
			supportMatch = supportOrder.match(order.lower())
			convoyMatch = convoyOrder.match(order.lower())

			if supportMatch != None:
				moveMatch = moveOrder.match(supportMatch.group(3))


	def connectTwoRegions(self, region1abbv, region2abbv):
		region1 = None
		region2 = None
		
		if region1abbv.lower() in self.regionDict.keys():
			region1 = self.regionDict[region1abbv.lower()]
		else:
			return -1

		if region2abbv.lower() in self.regionDict.keys():
			region2 = self.regionDict[region2abbv.lower()]
		else:
			return -1

		region1.addNeighbour(region2)
		region2.addNeighbour(region1)
		return 0

	def connectAllRegions(self, filename):
		f = open(filename)
		print('connecting regions')
		for line in f:
			parts = line.strip().split()
			if (self.connectTwoRegions(parts[0], parts[1]) == -1):
				print('Error connecting', parts[0], 'and', parts[1])
		f.close()
		print('regions connected')

	def endTurn(self):
		for unit in self.units:
			unit.ordered = False

		for region in self.regions:
			region.defensiveStrength = 0

		self.orders = []


class LandLockedTests(unittest.TestCase):
	def setUp(self):
		self.testGame = Game()
		self.testGame.regions = []
		self.testGame.units = []
		self.testGame.regionDict = {}

		self.testLocationA = Region('A', 'A', 0, 1)
		self.testLocationB = Region('B', 'B', 0, 2)
		self.testLocationC = Region('C', 'C', 0, 3)
		self.testLocationD = Region('D', 'D', 0, 7) # Neutral
		"""
		Test Region Layout
		-----
		|A|B|
		-----
		|C|D|
		-----
		All regions are land.
		Diagonal regions are NOT adjacent
		"""

		self.testGame.regions.append(self.testLocationA)
		self.testGame.regions.append(self.testLocationB)
		self.testGame.regions.append(self.testLocationC)
		self.testGame.regions.append(self.testLocationD)

		self.testGame.connectTwoRegions('A', 'B')
		self.testGame.connectTwoRegions('A', 'C')
		self.testGame.connectTwoRegions('B', 'D')
		self.testGame.connectTwoRegions('C', 'D')

		self.testUnit = Unit(0, self.testLocationA, 1)
		self.testLocationA.unit = self.testUnit

		self.testGame.units.append(self.testUnit)

	def test_hold(self):
		self.assertTrue(len(self.testGame.regions) == 4)
		#test.assertTrue(testLocationA.unit = )

if __name__ == '__main__':
    unittest.main()