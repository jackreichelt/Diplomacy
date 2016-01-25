class MoveOrder(object):
	"""
	The Order class represents a move order that a unit has been given.
	The unit shows which unit is being given the order.
	The location variable shows the location of that unit. (Redundant?)
	The strength is the effective strength of the action.
		1 base, plus 1 per support.
	The lowerOrders and higherOrders variables store the orders above and
		below it on the tree.
	inTree and resolved are markers to show stages of processing.
	paired is a list that shows all orders to be resolved simultaneously.
	"""
	target = None

	def __init__(self, unit, location, target):
		self.unit = unit
		self.location = location
		self.strength = 1
		self.target = target
		self.lowerOrders = []
		self.higherOrders = []
		self.inTree = False
		self.resolved = False
		self.paired = [self]

		self.unit.ordered = True

	def getType():
		return 'move'

	def buildTree(self):		
		self.inTree = True

		# Any MoveOrders that are targeting me.
		for area in self.location.neighbours:
			if area.unit != None:
				if area.unit.order.target == self.location and not area.unit.order.inTree:
					if area.unit.order.location == self.target:
						# Deadlocking with me. i.e. I'm targetting them too.
						self.paired.append(area.unit.order)
						area.unit.order.paired = self.paired
					else:
						# Just targetting me.
						self.higherOrders.append(area.unit.order)
					area.unit.order.buildTree()

		# The target location's order.
		if self.target.unit != None:
			if not self.target.unit.order.inTree:
				self.lowerOrders.append(self.target.unit.order)
		
		# Any MoveOrders that are targeting my target.
		for area in self.target.neighbours:
			if area != self and area.unit != None:
				if area.unit.order.inTree == False and area.unit.order.target == self.target:
					self.paired.append(area.unit.order)
					area.unit.order.paired = self.paired
					area.unit.order.buildTree()

		for node in self.lowerOrders:
			if not node.inTree:
				node.buildTree()
		for node in self.higherOrders:
			if not node.inTree:
				node.buildTree()

	def fail(self):
		if not self.resolved:
			self.strength = 1
			self.target = None
			self.location.defensiveStrength += 1
			self.resolved = True

	def resolveTree(self):
		for child in self.lowerOrders:
			if not child.resolved:
				child.resolveTree()

		self.resolve()

		for parent in self.higherOrders:
			parent.resolveTree()

	def resolve(self):
		if not self.resolved:
			# TODO: Need to add a special case for when units from two regions are
			# both moving into each other.
			if len(self.paired) > 1:

				for pair in self.paired[1:]:
					for child in pair.lowerOrders:
						child.resolve()

				maxStrength = 0
				strongest = []
				for order in self.paired:
					if order.strength > maxStrength:
						maxStrength = order.strength
						strongest = [order]
					elif order.strength == maxStrength:
						strongest.append(order)
				if len(strongest) == 1:
					print('resolving')
					strongest[1].resolve()
				for order in self.paired:
					print('failing')
					order.fail()
			else:
				if self.strength > self.target.defensiveStrength:
					# TODO: Mark defending unit for retreat
					self.unit.location = self.target
					self.location.unit = None
					self.target.unit = self.unit
					self.target.owner = self.unit.owner
				else:
					self.location.defensiveStrength += 1

				self.resolved = True

class HoldOrder(object):
	"""
	The HoldOrder class represents a unit being told to hold, or given no order..
	The unit shows which unit is being given the order.
	The location variable shows the location of that unit. (Redundant?)
	The strength is the effective strength of the action.
		1 base, plus 1 per support.
	The lowerOrders and higherOrders variables store the orders above and
		below it on the tree.
	"""
	target = None

	def __init__(self, unit, location):
		self.unit = unit
		self.location = location
		self.strength = 1
		self.target = None
		self.lowerOrders = []
		self.higherOrders = []
		self.inTree = False
		self.resolved = False

		self.success = False

		self.unit.ordered = True

	def getType():
		return 'hold'

	def buildTree(self):
		#print('Building Tree B')
		for area in self.location.neighbours:
			if area.unit != None:
				if area.unit.order.target == self and not area.unit.order.inTree:
					self.higherOrders.append(area.unit.order)
					area.unit.order.inTree = True
		self.inTree = True
		for node in self.lowerOrders:
			node.buildTree()
		for node in self.higherOrders:
			node.buildTree()
		#print('Tree Built')
			
	def resolveTree(self):
		for child in self.lowerOrders:
			if not child.resolved:
				child.resolveTree()

		self.resolve()

		for parent in self.higherOrders:
			parent.resolveTree()		

	def resolve(self):
		if not self.resolved:
			self.location.defensiveStrength += 1
			self.resolved = True

class NullOrder(object):
	"""
	The NullOrder class represents a region having no unit to order.
	This is used for determining if two otherwise disconnected units
		are attempting to take the same region.
	"""
	def __init__(self, location):
		self.unit = None
		self.location = location
		self.strength = 0
		self.target = None
		self.lowerOrders = []
		self.higherOrders = []
		self.inTree = True
		self.resolved = False

		self.success = False

		self.buildTree()
		self.resolve()

	def getType():
		return 'null'

	def buildTree(self):
		for area in self.location.neighbours:
			print('Reading neighbour', area.name)
			if area.unit:
				print('Unit found')
				if area.unit.order.target == self.location:
					print('Unit targetting me.')
					self.lowerOrders.append(area.unit.order)
					area.unit.order.higherOrders.append(self)
					area.unit.order.inTree = True

	def resolveTree(self):
		for child in self.lowerOrders:
			if not child.resolved:
				child.resolveTree()

		self.resolve()

		for parent in self.higherOrders:
			parent.resolveTree()

	def resolve(self):
		if not self.resolved:
			self.resolved = True
			highestOrder = None
			willResolve = True
			for order in self.lowerOrders:
				if not order.inTree:
					order.buildTree(True)
				for child in order.lowerOrders:
					child.resolve()
				if highestOrder == None:
					highestOrder = order
				else:
					if highestOrder.strength > order.strength:
						highestOrder = order
						willResolve = True
					elif highestOrder.strength == order.strength:
						willResolve = False
				print("Highest Strength:", highestOrder.strength)
				print("Will resolve:", willResolve)

			if not willResolve:
				for order in self.lowerOrders:
					order.location.defensiveStrength += 1
					order.resolved = True
			else:
				for order in self.lowerOrders:
					if order != highestOrder:
						order.location.defensiveStrength += 1
						order.resolved = True
					else:
						order.resolve()
