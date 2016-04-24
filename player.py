class Player:

	def __init__(self, name, oceanSpace, noOfShips=5):
		self.name = name
		self.oceanSpace = oceanSpace
		self.gameScore = 0
		self.noOfShips = noOfShips
		self.shipsDestroyed = 0
		self.shipPositions = []
		self.ready = False