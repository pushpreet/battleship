class Ocean:
	""" Ocean class maintains the state of the ocean for each player.

		Attributes:
			size -- size of the grid
			grid -- 2D list with the current state
	"""

	def __init__(self, size):
		""" Initialises grid with all spaces available """
		self.size = size
		self.grid = [ ['~' for _ in range(size)] for _ in range(size) ]

	def updateGrid(self, value, coordinates):
		for coordinate in coordinates:
			x, y = coordinate	#each coordinate is a tuple

			if (x > (self.size-1)) or (y > (self.size-1)):
				raise ValueError('coordinate out of scope', repr(coordinate))

		if value == '+':	#placing ships

			for coordinate in coordinates:
				x, y = coordinate

				if self.grid[x][y] == '~':
					self.markGrid(value, coordinate)

					self.markGrid('*', (x-1, y))
					self.markGrid('*', (x, y-1))
					self.markGrid('*', (x, y+1))
					self.markGrid('*', (x+1, y))

				else:
					raise ValueError('position not available')

			return True

		if value == 'x':	#attacked
			for coordinate in coordinates:
				x, y = coordinate

				if self.grid[x][y] == '+':
					self.markGrid(value, coordinate)

					self.markGrid('*', (x-1, y))
					self.markGrid('*', (x, y-1))
					self.markGrid('*', (x, y+1))
					self.markGrid('*', (x+1, y))

				elif self.grid[x][y] == '~':
					self.markGrid('-', coordinate)

				else:
					raise ValueError('position already attacked')

		if value == '~':	#remove ship
			for coordinate in coordinates:
				x, y = coordinate

				if self.grid[x][y] == '+':
					self.markGrid(value, coordinate)

					self.markGrid('~', (x-1, y))
					self.markGrid('~', (x, y-1))
					self.markGrid('~', (x, y+1))
					self.markGrid('~', (x+1, y))

					for x in range(0, self.size):
						for y in range(0, self.size):
							if self.grid[x][y] == '+':
								self.markGrid('*', (x-1, y))
								self.markGrid('*', (x, y-1))
								self.markGrid('*', (x, y+1))
								self.markGrid('*', (x+1, y))

				else:
					raise ValueError('position not available')

	def markGrid(self, value, position):
		x, y = position

		if x > (self.size-1) or (y > self.size-1) or (x < 0) or (y < 0):
			return False

		if value == '~':
			if self.grid[x][y] == '+' or self.grid[x][y] == '*':
				self.grid[x][y] = '~'

		if value == '+':
			if self.grid[x][y] == '~':
				self.grid[x][y] = '+'

		if value == 'x':
			if self.grid[x][y] == '+' or self.grid[x][y] == '~' or self.grid[x][y] == '*':
				self.grid[x][y] = 'x'

		if value == '-':
			if self.grid[x][y] == '+' or self.grid[x][y] == '~' or self.grid[x][y] == '*':
				self.grid[x][y] = '-'

		if value == '*':
			if self.grid[x][y] == '~':
				self.grid[x][y] = '*'

		return True

	def cleanGrid(self, new = False):
		for x in range(0, self.size):
			for y in range(0, self.size):
				if new == True:
					self.grid[x][y] = '~'

				else:
					if self.grid[x][y] == '*':
						self.grid[x][y] = '~'

	def spitOcean(self):
		for row in self.grid:
			for ele in row:
				print(ele + '   ',)

			print('\n')