from enum import Enum
import re

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
	"""docstring for Region"""

	def __init__(self, name, abbrev, myType,
				owner = Faction.neutral):
		self.name = name
		self.abbrev = abbrev
		self.myType = myType
		self.owner = owner
		self.neighbour = ()

	def __str__(self):
		return self.name

	def addNeighbour(self, neighbour):
		self.neighbours.append(neighbour)

	def changeOwner(self, newOwner):
		self.owner = newOwner

	def spawnUnit(self, unitType):
		newUnit = Unit(unitType, self)


class Unit(object):
	"""docstring for Unit"""

	def __init__(self, unitType, location, owner):
		self.unitType = unitType
		self.location = location
		self.owner = owner
		self.ordered = False

class Game(object):
	"""docstring for Game"""
	regions = []
	regionSet = []
	units = []
	orders = []
	abbrevDict = {}

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
			self.regionSet.append(parts[0])
			self.abbrevDict[parts[1].lower()] = parts[0]

	def readUnits(self, filename):
		f = open(filename)
		print('reading units')
		for line in f:
			parts = line.strip().split('\t')
			newUnit = Unit(Type.stringToInt(parts[0]), parts[1],
				Faction.stringToInt(parts[2]))
			self.units.append(newUnit)

	def newTurn(self):
		self.orders = []

	def addOrder(self, newOrder):
		self.orders.append(newOrder)

	def parseOrders(self):
		holdOrder = re.compile('^([af]|fleet|army) (...+)[ -](holds?)')
		moveOrder = re.compile('^([af]|fleet|army) (...+)[ -](...+)$')
		supportOrder = re.compile('^([af]|fleet|army) (...+) s (.*)$')
		convoyOrder = re.compile('^([af]|fleet|army) (...+) c (.*)$')

		defensiveStrength = {}
		actionStrength = {}

		holdQueue = []
		moveQueue = []
		supportQueue = []
		convoyQueue = []

		#split the orders into four categories
		for order in self.orders:
			moveMatch = moveOrder.match(order.lower())
			supportMatch = supportOrder.match(order.lower())
			convoyMatch = convoyOrder.match(order.lower())
			holdMatch = holdOrder.match(order.lower())
			if moveMatch != None and holdMatch == None and supportMatch == None\
					and convoyMatch == None:
				moveQueue.append((order, moveMatch))
				unit.ordered = True
				#print(order, 'move', moveMatch)
			elif supportMatch != None and convoyMatch == None:
				supportQueue.append((order, supportMatch))
				unit.ordered = True
				#print(order, 'support', supportMatch)
			elif convoyMatch != None:
				convoyQueue.append((order, convoyMatch))
				unit.ordered = True
				#print(order, 'convoy', convoyMatch)
			else:
				holdMatch = holdOrder.match(order.lower())
				#print(order, 'hold', holdMatch)
				if holdMatch != None:

					region = holdMatch.group(2)
					
					if region in self.abbrevDict.keys():
						region = self.abbrevDict[region]
					else:
						abbrev = False

					for unit in self.units:
						if Type.stringToInt(holdMatch.group(1)) == unit.unitType and\
								region == unit.location:
							defensiveStrength[region.lower()] = 1
							print('here')
							unit.ordered = True


		for unit in self.units:
			print(unit.owner, unit.unitType, unit.location, unit.ordered)
			if unit.ordered == False:
				defensiveStrength[unit.location.lower()] = 1
			unit.ordered = False

		for region in defensiveStrength.keys():
			print(region, defensiveStrength[region])

	def connectTwoRegions(self, region1abbv, region2abbv):
		region1 = None
		region2 = None
		for region in regions:
			if region.abbrev == region1abbv:
				region1 = region
			elif region.abbrev == region2abbv:
				region2 = region

		if region1 == None or region2 == None:
			return -1

		region1.addNeighbour(region2)
		region2.addNeighbour(region1)
		return 0

	def connectAllRegions(self, filename):
		f = open(filename)
		print('connecting regions')
		for line in f:
			parts = line.strip().split()
			if (connectTwoRegions(parts[0], parts[1]) == -1):
				print('Error connecting', parts[0], 'and', parts[1])




game = Game()
#for region in game.regions:
#	if region.owner != Faction.neutral:
#		print(region.name, region.owner, Faction.intToString(region.owner))
#for unit in sorted(game.units, key=lambda unit: unit.owner):
#	print(Faction.intToString(unit.owner), unit.location,
#		Type.intToString(unit.unitType))

game.addOrder('F Lon Hold')
game.addOrder('a par-bre')
game.parseOrders()