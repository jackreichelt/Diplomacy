class MoveOrder(object):
	"""
	The Order class represents a move order that a unit has been given.
	The unit shows which unit is being given the order.
	The location variable shows the location of that unit. (Redundant?)
	The strength is the effective strength of the action.
		1 base, plus 1 per support.
	The lowerOrders and higherOrders variables store the 

	Possibly also need to make different Order classes, on the same template.
	This would allow a different resolution command, and such.
	"""
	target = None

	def __init__(self, unit, location, target):
		self.unit = unit
		self.location = location
		self.strength = 1
		self.target = target
		self.lowerOrders = []
		self.higherOrders = []
		self.resolved = False

		self.unit.ordered = True

	def buildTree(self):
		for area in self.location.neighbours:
			if area.unit != None:
				if area.unit.order.target == self.location:
					self.higherOrders.append(area.unit.order)
				if area == self.target:
					self.lowerOrders.append(area.unit.order)
					

	def resolve(self):
		for child in self.lowerOrders:
			child.resolve()
		
		if not self.resolved:
			# TODO: Need to add a special case for when units from two regions are
			# both moving into each other.
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
	The Order class represents a move order that a unit has been given.
	The unit shows which unit is being given the order.
	The location variable shows the location of that unit. (Redundant?)
	The strength is the effective strength of the action.
		1 base, plus 1 per support.
	The lowerOrders and higherOrders variables store the 

	Possibly also need to make different Order classes, on the same template.
	This would allow a different resolution command, and such.
	"""
	target = None

	def __init__(self, unit, location):
		self.unit = unit
		self.location = location
		self.strength = 1
		self.target = None
		self.lowerOrders = []
		self.higherOrders = []
		self.resolved = False

		self.success = False

		self.unit.ordered = True

	def buildTree(self):
		for area in self.location.neighbours:
			if area.unit != None:
				if area.unit.order.target == self:
					self.higherOrders.append(area.unit.order)
					

	def resolve(self):
		for child in self.lowerOrders:
			child.resolve()

		if not self.resolved:
			self.location.defensiveStrength += 1
			self.resolved = True

		for parent in self.higherOrders:
			parent.resolve()