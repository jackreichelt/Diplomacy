class MoveOrder(object):
	"""
	The Order class represents a move order that a unit has been given.
	The unit shows which unit is being given the order.
	The location variable shows the location of that unit. (Redundant?)
	The strength is the effective strength of the action.
		1 base, plus 1 per support.
	The lowerOrders and higherOrders variables store the orders above and
		below it on the tree.
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
		self.paired = None

		self.unit.ordered = True

	def getType():
		return 'move'

	def buildTree(self):
		#print('Building Tree A')
		for area in self.location.neighbours:
			if area.unit != None:
				if area.unit.order.target == self.location and not area.unit.order.inTree:
					if self.target == area.unit.order.location:
						self.paired = area.unit.order
						area.unit.order.paired = self
						area.unit.order.inTree = True
						self.paired.buildTree()
					else:
						self.higherOrders.append(area.unit.order)
						area.unit.order.inTree = True
				if area == self.target and not area.unit.order.inTree:
					self.lowerOrders.append(area.unit.order)
					area.unit.order.inTree = True
			#else:
			#	NullOrder(area)
		self.inTree = True
		for node in self.lowerOrders:
			node.buildTree()
		for node in self.higherOrders:
			node.buildTree()
		#print('Tree Built')
					

	def resolve(self):
		for child in self.lowerOrders:
			child.resolve()
		
		if not self.resolved:
			# TODO: Need to add a special case for when units from two regions are
			# both moving into each other.
			if self.paired:
				if self.strength < self.paired.strength:
					# TODO: Mark self for retreat
					self.location.unit = sef.paired.unit
					self.location.owner = self.paired.unit.owner
					self.paired.unit.location = self.location
					self.paired.location.unit = None
				elif self.strength > self.paired.strength:
					# TODO: Mark defending unit for retreat
					self.unit.location = self.target
					self.location.unit = None
					self.target.unit = self.unit
					self.target.owner = self.unit.owner
				self.paired.resolved = True
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

		for parent in self.higherOrders:
			parent.resolve()
		# if self.strength > self.target.defensiveStrength:
		# #   self.success = True
		# #   return([self.unit, self.location, self.target])
		# # else:
		# #   self.location.defensiveStrength += 1
		# 	self.location.unit = None
		# 	self.target.unit = self.unit
		# 	self.unit.location = self.target
		# 	self.target.owner = self.location.owner
		# else:
		# 	self.location.defensiveStrength += 1
		# #TODO: Mark unit in target location for retreat.

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
					

	def resolve(self):
		for child in self.lowerOrders:
			child.resolve()

		if not self.resolved:
			self.location.defensiveStrength += 1
			self.resolved = True

		for parent in self.higherOrders:
			parent.resolve()

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
			if area.unit:
				if area.unit.order.target == self.location:
					self.lowerOrders.append(area.unit.order)
					area.unit.order.higherOrders.append(self)
					area.unit.order.inTree = True

	def resolve(self):
		if not self.resolved:
			self.resolved = True
			highestOrder = None
			willResolve = True
			for order in self.lowerOrders:
				order.buildTree()
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

			if not willResolve:
				for order in orders:
					order.location.defensiveStrength += 1
					order.resolved = True
			else:
				for order in orders:
					if order != highestOrder:
						order.location.defensiveStrength += 1
						order.resolved = True
					else:
						order.resolve()
