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
    print('Unit at region {}, targeting {}, with strength {} against strength {}'.format(self.location.name, self.target.name, self.strength, self.target.defensiveStrength))
    if self.target.defensiveStrength < self.strength:
      print('  So it is approved.')
      self.approved = True
    else:
      self.location.defensiveStrength += 1
      self.resolved = True

  def enact(self):
    order_strengths = {}

    print("Checking region: {}".format(self.target.name))

    for area in self.target.neighbours:
      print('  Adjacent region: {}.'.format(area.name))
      if area.unit != None:
        print('    Region has a unit with order type {}.'.format(area.unit.order.type))
        print('      Targeting {}. Approval status: {}.'.format(area.unit.order.target.name, area.unit.order.approved))
        if area.unit.order.target == self.target and area.unit.order.approved:
          print('      Approved.')
          if area.unit.order.strength in order_strengths:
            order_strengths[area.unit.order.strength].append(area.unit.order)
          else:
            order_strengths[area.unit.order.strength] = [(area.unit.order)]
          area.unit.order.resolved = True

    print('Order Strengths: {}'.format(order_strengths))

    max_strength = max(order_strengths)

    if len(order_strengths[max_strength]) == 1:
      order = order_strengths[max_strength][0]
      order.unit.move_to(order.target)

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
