from ocean import Ocean
from player import Player
import socket
import select
import time

class BattleshipGame:

	def __init__(self):
		self.role = 'server'
		self.sock = socket.socket()
		self.conn = socket.socket()
		self.oceanSize = 5
		self.player = Player('Player', Ocean(self.oceanSize))
		self.opponent = Player('Opponent', Ocean(self.oceanSize))
		self.host = ''
		self.port = -1
		
		self.gameState = 'IDLE'

	def __del__(self):
		self.conn.close()

	def newGame(self, port=27030):
		if port < 0:
			return False

		self.port = port
		self.sock.bind((self.host, self.port))
		self.sock.listen(0)

		self.gameState = 'WAITING FOR PLAYER'

		self.conn, addr = self.sock.accept()

		print("Got connection from", addr)
		self.gameState = 'SETTING UP'

		self.gameSetup()

	def joinGame(self, host, port):
		self.role = 'client'

		if host == 'localhost':
			self.host = socket.gethostname()
		else:
			self.host = host

		self.port = int(port)

		self.gameState = 'CONNECTING'
		self.conn.connect((self.host, self.port))
		
		self.gameState = 'SETTING UP'

		self.gameSetup()

	def gameSetup(self):
		self.conn.send(bytes('SET ' + self.player.name + ' ' +str(self.oceanSize) + ':', 'UTF-8'))

		inMessage = self.recvMessage()
		gameData = inMessage.split()

		if gameData[0] == 'SET':
			self.opponent.name = gameData[1]
			self.opponent.oceanSpace.__init__(int(gameData[2]))

		self.conn.send(bytes('RDY' + ':', 'UTF-8'))

		inMessage = self.recvMessage()
		if inMessage == 'RDY':
			self.gameState = 'PLACING SHIPS'

	def recvMessage(self):
		isReadable = [self.conn]

		readAvail, writeAvail, errorAvail = select.select(isReadable, [], [], 0.1)

		if readAvail:
			byte = ''
			message = ''
			while True:
				byte = self.conn.recv(1).decode('UTF-8')
				
				if byte == ':':
					break
				else:
					message += byte

			return message

	def placeShip(self, row, col):
		if (row, col) in self.player.shipPositions:
			self.player.oceanSpace.updateGrid('~', [(row, col)])
			self.player.shipPositions.remove((row, col))

			if self.gameState == 'SHIPS PLACED':
				self.gameState = 'PLACING SHIPS'
				return self.gameState

		else:
			if len(self.player.shipPositions) < self.player.noOfShips:
				if self.player.oceanSpace.updateGrid('+', [(row, col)]):
					self.player.shipPositions.append((row, col))

			if len(self.player.shipPositions) == self.player.noOfShips:
				self.gameState = 'SHIPS PLACED'
				return self.gameState

	def attackShip(self, row, col):
		if self.opponent.oceanSpace.grid[row][col] == '~':
			self.conn.send(bytes('ATK ' + str(row) + ' ' + str(col) + ':', 'UTF-8'))
			msg = self.parseIncoming()

			if msg == 'LOST':
				self.gameState = 'WON'
				self.opponent.oceanSpace.updateGrid('+', [(row, col)])
				self.opponent.oceanSpace.updateGrid('x', [(row, col)])
				self.conn.close()

			elif msg == 'HIT':
				self.gameState = 'WAITING FOR OPPONENT'
				self.opponent.oceanSpace.updateGrid('+', [(row, col)])
				self.opponent.oceanSpace.updateGrid('x', [(row, col)])

			elif msg == 'MISS':
				self.gameState = 'WAITING FOR OPPONENT'
				self.opponent.oceanSpace.updateGrid('x', [(row, col)])

			return True

		elif self.opponent.oceanSpace.grid[row][col] == 'x' or self.opponent.oceanSpace.grid[row][col] == '-' or self.opponent.oceanSpace.grid[row][col] == '*':
			return False

	def declareReady(self):
		if self.gameState == 'SHIPS PLACED':
			self.gameState = 'SHIPS READY'
			self.player.ready = True
			self.player.oceanSpace.cleanGrid()

			self.conn.send(bytes('RDY SHIPS' + ':', 'UTF-8'))

			if self.opponent.ready == True:
				if self.role == 'server':
					self.gameState = 'WAITING FOR INPUT'
				else:
					self.gameState = 'WAITING FOR OPPONENT'

	def parseIncoming(self):
		inMessage = self.recvMessage()

		if inMessage:
			inMessage = inMessage.split()

			if inMessage[0] == 'RDY':
				if inMessage[1] == 'SHIPS':
					self.opponent.ready = True

					if self.player.ready == True:
						if self.role == 'server':
							self.gameState = 'WAITING FOR INPUT'
						else:
							self.gameState = 'WAITING FOR OPPONENT'

					return 'OPPONENT READY'

			if inMessage[0] == 'ATK':
				row = int(inMessage[1])
				col = int(inMessage[2])

				self.gameState = 'WAITING FOR INPUT'

				if self.player.oceanSpace.grid[row][col] == '+':
					self.player.oceanSpace.updateGrid('x', [(row, col)])
					self.player.shipsDestroyed += 1

					if self.player.shipsDestroyed == self.player.noOfShips:
						self.gameState = 'LOST'
						self.conn.send(bytes('REP LOST' + ':', 'UTF-8'))
						self.conn.close()
						
					else:
						self.conn.send(bytes('REP HIT' + ':', 'UTF-8'))

				else:
					self.player.oceanSpace.updateGrid('x', [(row, col)])
					self.conn.send(bytes('REP MISS' + ':', 'UTF-8'))

			if inMessage[0] == 'REP':
				return inMessage[1]

	def setPlayerName(self, playerName):
		self.player.name = str(playerName)