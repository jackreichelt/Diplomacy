from Diplomacy import *


class LandLockedUnopposedTests(unittest.TestCase):
	def setUp(self):
		self.testGame = Game(True)
		self.testGame.regions = []
		self.testGame.units = []
		self.testGame.regionDict = {}

		self.testLocationA = Region('aaa', 'aaa', 0, 1)
		self.testLocationB = Region('bbb', 'bbb', 0, 2)
		self.testLocationC = Region('ccc', 'ccc', 0, 3)
		self.testLocationD = Region('ddd', 'ddd', 0, 7) # Neutral
		"""
		Test Region Layout
		-----
		|A|B|
		-----
		|C|D|
		-----
		All regions are land.
		Diagonal regions ARE NOT adjacent.
		Regions A, B, and C are all owned by different people.
		Region D is unowned.
		Region A has a unit in it.
		"""
		self.testGame.addRegion(self.testLocationA)
		self.testGame.addRegion(self.testLocationB)
		self.testGame.addRegion(self.testLocationC)
		self.testGame.addRegion(self.testLocationD)

		self.testGame.connectTwoRegions('aaa', 'bbb')
		self.testGame.connectTwoRegions('aaa', 'ccc')
		self.testGame.connectTwoRegions('bbb', 'ddd')
		self.testGame.connectTwoRegions('ccc', 'ddd')
		#self.testGame.connectTwoRegions('aaa', 'ddd')
		#self.testGame.connectTwoRegions('bbb', 'ccc')

		self.testUnit = Unit(0, self.testLocationA, 1)
		self.testLocationA.unit = self.testUnit

		self.testGame.units.append(self.testUnit)

	def test_hold(self):
		self.assertTrue(len(self.testGame.regions) == 4)

		self.assertEqual(self.testUnit.location, self.testLocationA)

		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 2)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 7)
	
	def test_move(self):
		self.testGame.addOrder('A aaa-bbb')
		self.testGame.resolveOrders()
		self.testGame.endTurn()

		self.assertEqual(self.testUnit.location, self.testLocationB)

		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 1)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 7)

	def test_invalid_move(self):
		self.testGame.addOrder('A aaa-ddd')
		self.testGame.resolveOrders()
		self.testGame.endTurn()

		self.assertEqual(self.testUnit.location, self.testLocationA)

		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 2)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 7)

class LandLockedOpposedTests(unittest.TestCase):
	def setUp(self):
		self.testGame = Game(True)
		self.testGame.regions = []
		self.testGame.units = []
		self.testGame.regionDict = {}

		self.testLocationA = Region('aaa', 'aaa', 0, 1)
		self.testLocationB = Region('bbb', 'bbb', 0, 2)
		self.testLocationC = Region('ccc', 'ccc', 0, 3)
		self.testLocationD = Region('ddd', 'ddd', 0, 7) # Neutral
		"""
		Test Region Layout
		-----
		|A|B|
		-----
		|C|D|
		-----
		All regions are land.
		Diagonal regions ARE NOT adjacent.
		Regions A, B, and C are all owned by different people.
		Region D is unowned.
		Region A has a unit in it.
		Region B has a unit in it.
		"""
		self.testGame.addRegion(self.testLocationA)
		self.testGame.addRegion(self.testLocationB)
		self.testGame.addRegion(self.testLocationC)
		self.testGame.addRegion(self.testLocationD)

		self.testGame.connectTwoRegions('aaa', 'bbb')
		self.testGame.connectTwoRegions('aaa', 'ccc')
		self.testGame.connectTwoRegions('bbb', 'ddd')
		self.testGame.connectTwoRegions('ccc', 'ddd')
		#self.testGame.connectTwoRegions('aaa', 'ddd')
		#self.testGame.connectTwoRegions('bbb', 'ccc')

		self.testUnitA = Unit(0, self.testLocationA, 1)
		self.testLocationA.unit = self.testUnitA

		self.testUnitB = Unit(0, self.testLocationB, 2)
		self.testLocationB.unit = self.testUnitB

		self.testGame.units.append(self.testUnitA)
		self.testGame.units.append(self.testUnitB)
	
	def test_attack(self):
		self.testGame.addOrder('A aaa-bbb')
		self.testGame.resolveOrders()
		self.testGame.endTurn()

		self.assertEqual(self.testUnitA.location, self.testLocationA)

		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 2)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 7)

	def test_attackAndEvacuate(self):
		self.testGame.addOrder('A aaa-bbb')
		self.testGame.addOrder('A bbb-ddd')

		self.testGame.resolveOrders()
		self.testGame.endTurn()

		#print('Loc A:', self.testUnitA.location == self.testLocationA)
		self.assertEqual(self.testUnitA.location, self.testLocationB)
		self.assertEqual(self.testUnitB.location, self.testLocationD)

		self.assertEqual(self.testLocationA.unit, None)
		self.assertEqual(self.testLocationD.unit, self.testUnitB)
		self.assertEqual(self.testLocationB.unit, self.testUnitA)
		
		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 1)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 2)

	def test_attackAndEvacuateRev(self):
		self.testGame.addOrder('A bbb-ddd')
		self.testGame.addOrder('A aaa-bbb')

		self.testGame.resolveOrders()
		self.testGame.endTurn()

		#print('Loc A:', self.testUnitA.location == self.testLocationA)
		self.assertEqual(self.testUnitA.location, self.testLocationB)
		self.assertEqual(self.testUnitB.location, self.testLocationD)

		self.assertEqual(self.testLocationA.unit, None)
		self.assertEqual(self.testLocationD.unit, self.testUnitB)
		self.assertEqual(self.testLocationB.unit, self.testUnitA)
		
		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 1)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 2)

	def test_attackDeadlock(self):
		#print('<<HERE>>')
		self.testGame.addOrder('A aaa-bbb')
		self.testGame.addOrder('A bbb-aaa')

		self.testGame.resolveOrders()
		self.testGame.endTurn()
		#print('<<AND HERE>>')

		#print('Loc A:', self.testUnitA.location == self.testLocationA)
		self.assertEqual(self.testUnitA.location, self.testLocationA)
		self.assertEqual(self.testUnitB.location, self.testLocationB)

		self.assertEqual(self.testLocationA.unit, self.testUnitA)
		self.assertEqual(self.testLocationB.unit, self.testUnitB)
		self.assertEqual(self.testLocationD.unit, None)
		
		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 2)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 7)

class LandLockedThreeFactionTests(unittest.TestCase):
	def setUp(self):
		self.testGame = Game(True)
		self.testGame.regions = []
		self.testGame.units = []
		self.testGame.regionDict = {}

		self.testLocationA = Region('aaa', 'aaa', 0, 1)
		self.testLocationB = Region('bbb', 'bbb', 0, 2)
		self.testLocationC = Region('ccc', 'ccc', 0, 3)
		self.testLocationD = Region('ddd', 'ddd', 0, 7) # Neutral
		"""
		Test Region Layout
		-----
		|A|B|
		-----
		|C|D|
		-----
		All regions are land.
		Diagonal regions ARE NOT adjacent.
		Regions A, B, and C are all owned by different people.
		Region D is unowned.
		Region A has a unit in it.
		Region B has a unit in it.
		"""
		self.testGame.addRegion(self.testLocationA)
		self.testGame.addRegion(self.testLocationB)
		self.testGame.addRegion(self.testLocationC)
		self.testGame.addRegion(self.testLocationD)

		self.testGame.connectTwoRegions('aaa', 'bbb')
		self.testGame.connectTwoRegions('aaa', 'ccc')
		self.testGame.connectTwoRegions('bbb', 'ddd')
		self.testGame.connectTwoRegions('ccc', 'ddd')
		#self.testGame.connectTwoRegions('aaa', 'ddd')
		#self.testGame.connectTwoRegions('bbb', 'ccc')

		self.testUnitA = Unit(0, self.testLocationA, 1)
		self.testLocationA.unit = self.testUnitA

		self.testUnitB = Unit(0, self.testLocationB, 2)
		self.testLocationB.unit = self.testUnitB

		self.testUnitC = Unit(0, self.testLocationD, 3)
		self.testLocationD.unit = self.testUnitC

		self.testGame.units.append(self.testUnitA)
		self.testGame.units.append(self.testUnitB)
		self.testGame.units.append(self.testUnitC)

	def test_stalledAttack(self):
		#print('<<HERE>>')
		self.testGame.addOrder('A aaa-bbb')
		self.testGame.addOrder('A bbb-ddd')
		self.testGame.resolveOrders()
		self.testGame.endTurn()
		#print('<<AND HERE>>')

		self.assertEqual(self.testUnitA.location, self.testLocationA)
		self.assertEqual(self.testUnitB.location, self.testLocationB)
		self.assertEqual(self.testUnitC.location, self.testLocationD)

		self.assertEqual(self.testLocationA.unit, self.testUnitA)
		self.assertEqual(self.testLocationD.unit, self.testUnitC)
		self.assertEqual(self.testLocationB.unit, self.testUnitB)
		
		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 2)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 7)

class LandLockedTriangleLoop(unittest.TestCase):
	def setUp(self):
		self.testGame = Game(True)
		self.testGame.regions = []
		self.testGame.units = []
		self.testGame.regionDict = {}

		self.testLocationA = Region('aaa', 'aaa', 0, 1)
		self.testLocationB = Region('bbb', 'bbb', 0, 2)
		self.testLocationC = Region('ccc', 'ccc', 0, 3)
		"""
		Test Region Layout
		-----
		|A|B|
		-----
		| C |
		-----
		All regions are land.
		Diagonal regions ARE NOT adjacent.
		Regions A, B, and C are all owned by different people.
		Region A has a unit in it.
		Region B has a unit in it.
		Region C has a unit in it.
		"""
		self.testGame.addRegion(self.testLocationA)
		self.testGame.addRegion(self.testLocationB)
		self.testGame.addRegion(self.testLocationC)

		self.testGame.connectTwoRegions('aaa', 'bbb')
		self.testGame.connectTwoRegions('aaa', 'ccc')
		#self.testGame.connectTwoRegions('bbb', 'ddd')
		#self.testGame.connectTwoRegions('ccc', 'ddd')
		#self.testGame.connectTwoRegions('aaa', 'ddd')
		self.testGame.connectTwoRegions('bbb', 'ccc')

		self.testUnitA = Unit(0, self.testLocationA, 1)
		self.testLocationA.unit = self.testUnitA

		self.testUnitB = Unit(0, self.testLocationB, 2)
		self.testLocationB.unit = self.testUnitB

		self.testUnitC = Unit(0, self.testLocationC, 3)
		self.testLocationC.unit = self.testUnitC

		self.testGame.units.append(self.testUnitA)
		self.testGame.units.append(self.testUnitB)
		self.testGame.units.append(self.testUnitC)

	def test_ThreeLoop(self):
		#print('<<HERE>>')
		self.testGame.addOrder('A aaa-bbb')
		self.testGame.addOrder('A bbb-ccc')
		self.testGame.addOrder('A ccc-aaa')
		self.testGame.resolveOrders()
		self.testGame.endTurn()
		#print('<<AND HERE>>')

		self.assertEqual(self.testUnitA.location, self.testLocationB)
		self.assertEqual(self.testUnitB.location, self.testLocationC)
		self.assertEqual(self.testUnitC.location, self.testLocationA)

		self.assertEqual(self.testLocationA.unit, self.testUnitC)
		self.assertEqual(self.testLocationB.unit, self.testUnitA)
		self.assertEqual(self.testLocationC.unit, self.testUnitB)
		
		self.assertEqual(self.testLocationA.owner, 3)
		self.assertEqual(self.testLocationB.owner, 1)
		self.assertEqual(self.testLocationC.owner, 2)

class LandLockedSquareLoop(unittest.TestCase):
	def setUp(self):
		self.testGame = Game(True)
		self.testGame.regions = []
		self.testGame.units = []
		self.testGame.regionDict = {}

		self.testLocationA = Region('aaa', 'aaa', 0, 1)
		self.testLocationB = Region('bbb', 'bbb', 0, 2)
		self.testLocationC = Region('ccc', 'ccc', 0, 3)
		self.testLocationD = Region('ddd', 'ddd', 0, 4)
		"""
		Test Region Layout
		-----
		|A|B|
		-----
		|D|C|
		-----
		All regions are land.
		Diagonal regions ARE NOT adjacent.
		Regions A, B, C, and D are all owned by different people.
		Region A has a unit in it.
		Region B has a unit in it.
		Region C has a unit in it.
		Region D has a unit in it.
		"""
		self.testGame.addRegion(self.testLocationA)
		self.testGame.addRegion(self.testLocationB)
		self.testGame.addRegion(self.testLocationC)
		self.testGame.addRegion(self.testLocationD)

		self.testGame.connectTwoRegions('aaa', 'bbb')
		self.testGame.connectTwoRegions('bbb', 'ccc')
		self.testGame.connectTwoRegions('ccc', 'ddd')
		self.testGame.connectTwoRegions('ddd', 'aaa')

		self.testUnitA = Unit(0, self.testLocationA, 1)
		self.testLocationA.unit = self.testUnitA

		self.testUnitB = Unit(0, self.testLocationB, 2)
		self.testLocationB.unit = self.testUnitB

		self.testUnitC = Unit(0, self.testLocationC, 3)
		self.testLocationD.unit = self.testUnitC

		self.testUnitD = Unit(0, self.testLocationD, 4)
		self.testLocationD.unit = self.testUnitD

		self.testGame.units.append(self.testUnitA)
		self.testGame.units.append(self.testUnitB)
		self.testGame.units.append(self.testUnitC)
		self.testGame.units.append(self.testUnitD)

	def test_fourloop(self):
		#print('<<HERE>>')
		self.testGame.addOrder('A aaa-bbb')
		self.testGame.addOrder('A bbb-ccc')
		self.testGame.addOrder('A ccc-ddd')
		self.testGame.addOrder('A ddd-aaa')
		self.testGame.resolveOrders()
		self.testGame.endTurn()
		#print('<<AND HERE>>')

		self.assertEqual(self.testUnitA.location, self.testLocationB)
		self.assertEqual(self.testUnitB.location, self.testLocationC)
		self.assertEqual(self.testUnitC.location, self.testLocationD)
		self.assertEqual(self.testUnitD.location, self.testLocationA)

		self.assertEqual(self.testLocationA.unit, self.testUnitD)
		self.assertEqual(self.testLocationB.unit, self.testUnitA)
		self.assertEqual(self.testLocationC.unit, self.testUnitB)
		self.assertEqual(self.testLocationD.unit, self.testUnitC)
		
		self.assertEqual(self.testLocationA.owner, 4)
		self.assertEqual(self.testLocationB.owner, 1)
		self.assertEqual(self.testLocationC.owner, 2)
		self.assertEqual(self.testLocationD.owner, 3)

class LandDiagonalUnits(unittest.TestCase):
	def setUp(self):
		self.testGame = Game(True)
		self.testGame.regions = []
		self.testGame.units = []
		self.testGame.regionDict = {}

		self.testLocationA = Region('aaa', 'aaa', 0, 1)
		self.testLocationB = Region('bbb', 'bbb', 0, 2)
		self.testLocationC = Region('ccc', 'ccc', 0, 3)
		self.testLocationD = Region('ddd', 'ddd', 0, 4)
		"""
		Test Region Layout
		-----
		|A|B|
		-----
		|D|C|
		-----
		All regions are land.
		Diagonal regions ARE NOT adjacent.
		Regions A, B, C, and D are all owned by different people.
		Region A has a unit in it.
		Region C has a unit in it.
		"""
		self.testGame.addRegion(self.testLocationA)
		self.testGame.addRegion(self.testLocationB)
		self.testGame.addRegion(self.testLocationC)
		self.testGame.addRegion(self.testLocationD)

		self.testGame.connectTwoRegions('aaa', 'bbb')
		self.testGame.connectTwoRegions('bbb', 'ccc')
		self.testGame.connectTwoRegions('ccc', 'ddd')
		self.testGame.connectTwoRegions('ddd', 'aaa')

		self.testUnitA = Unit(0, self.testLocationA, 1)
		self.testLocationA.unit = self.testUnitA

		self.testUnitC = Unit(0, self.testLocationC, 3)
		self.testLocationD.unit = self.testUnitC

		self.testGame.units.append(self.testUnitA)
		self.testGame.units.append(self.testUnitC)

	def test_bounce(self):
		#print('<<HERE>>')
		self.testGame.addOrder('A aaa-bbb')
		self.testGame.addOrder('A ccc-bbb')
		self.testGame.resolveOrders()
		self.testGame.endTurn()
		#print('<<AND HERE>>')

		self.assertEqual(self.testUnitA.location, self.testLocationA)
		self.assertEqual(self.testUnitC.location, self.testLocationC)

		self.assertEqual(self.testLocationA.unit, self.testUnitA)
		self.assertEqual(self.testLocationB.unit, None)
		self.assertEqual(self.testLocationC.unit, self.testUnitC)
		self.assertEqual(self.testLocationD.unit, None)
		
		self.assertEqual(self.testLocationA.owner, 1)
		self.assertEqual(self.testLocationB.owner, 2)
		self.assertEqual(self.testLocationC.owner, 3)
		self.assertEqual(self.testLocationD.owner, 4)


if __name__ == '__main__':
		unittest.main()