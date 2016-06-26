TARGETING_ORDER_PRIORITIES = { # Ordering for when the first key is targeting the second key.
  'hold':    {'hold': None,     'move': None,     'support': None,     'convoy': None},
  'move':    {'hold': 'before', 'move': 'before', 'support': 'before', 'convoy': 'before'},
  'support': {'hold': 'after',  'move': 'after',  'support': 'after',  'convoy': 'after'},
  'convoy':  {'hold': None,     'move': 'after',  'support': 'after',  'convoy': 'after'}
}

TARGETED_ORDER_PRIORITIES = { # Ordering for when the first key is targeted by the second key.
  'hold':    {'hold': None, 'move': 'after', 'support': 'before', 'convoy': None},
  'move':    {'hold': None, 'move': 'after', 'support': 'before', 'convoy': 'before'},
  'support': {'hold': None, 'move': 'after', 'support': 'before', 'convoy': 'before'},
  'convoy':  {'hold': None, 'move': 'after', 'support': 'before', 'convoy': 'before'}
}

class Order(object):
  """
  The Order class is the general class to represent an order.
  """

  def __init__(self, unit, location):
    self.unit = unit
    self.location = location
    self.target = None
    self.type = None
    self.strength = 1
    self.before = []
    self.after = []
    self.inTree = False
    self.processed = False
    self.approved = False
    self.resolved = False

    self.unit.ordered = True

  def build_graph(self):
    self.inTree = True
    for area in self.location.neighbours:
      if area.unit != None:
        if area.unit.order.inTree == False:
          # area.unit.order.inTree = True
          if area == self.target:
            if TARGETING_ORDER_PRIORITIES[self.type][area.unit.order.type] == 'before':
              self.before.append(area.unit.order)
              area.unit.order.after.append(self)
            elif TARGETING_ORDER_PRIORITIES[self.type][area.unit.order.type] == 'after':
              self.after.append(area.unit.order)
              area.unit.order.before.append(self)
          elif area.unit.order.target == self.location:
            if TARGETED_ORDER_PRIORITIES[self.type][area.unit.order.type] == 'before':
              self.before.append(area.unit.order)
              area.unit.order.after.append(self)
            elif TARGETED_ORDER_PRIORITIES[self.type][area.unit.order.type] == 'after':
              self.after.append(area.unit.order)
              area.unit.order.before.append(self)

    for order in self.before + self.after:
      if order.inTree == False:
        order.build_graph()

  def process_graph(self):
    for order in self.before:
      if order.processed == False:
        order.process_graph()

    if self.processed == False:
      self.validate()
      self.processed = True

    for order in self.after:
      if order.processed == False:
        order.process_graph()

class Move(Order):
  """
  The Move class specifies a Movement or Attack order (these are identical).
  """

  def __init__(self, unit, location, target):
    Order.__init__(self, unit, location)
    self.type = 'move'
    self.target = target

  def validate(self):
    if self.target.defensiveStrength < self.strength:
      self.approved = True
      return self.target
    else:
      self.location.defensiveStrength += 1
      self.resolved = True

  def enact(self):
    self.unit.move_to(self.target)
    self.resolved = True

class Hold(Order):
  """
  The Move class specifies a defensive action, or no specified order.
  """

  def __init__(self, unit, location):
    Order.__init__(self, unit, location)
    self.type = 'hold'

  def validate(self):
    self.approved = True
    self.location.defensiveStrength += 1

  def enact(self):
    pass