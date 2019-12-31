import pygame
from display import *

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Sudoku Solver")

class Board:
	# Initialize
	def __init__(this):
		this.board = [[0,0,0,5,4,0,7,0,6],
					  [0,3,5,0,0,0,0,0,0],
					  [0,8,6,0,0,0,3,0,0],
					  [0,1,0,0,0,0,0,0,0],
					  [9,0,7,0,0,5,2,0,0],
					  [0,0,0,2,7,0,0,0,0],
					  [0,0,2,9,0,0,5,6,0],
					  [6,9,0,7,5,0,0,0,2],
					  [0,0,0,0,0,0,0,1,4]]
	# Board methods
	def getBoard(this):
		return this.board

	def editBoard(this, coords, val):
		this.board[coords[0]][coords[1]] = val

	def printBoard(this):
		y = 20 # +55
		for row in this.board:
			x = 35 # +80
			for col in row:
				createButton(str(col), x, y, 80, 55, (255,255,255), (235,235,235))
				x += 80
			y += 55
		pygame.display.update()
		'''for l in this.board:
			print(l)'''

	def printBoardText(this):
		for l in this.board:
			print(l)

	# Validating methods
	def checkBoard(this):
		for x in range(0, 9):
			if (not this.checkQuadrant(x)) or (not this.checkRow(x)) or (not this.checkColumn(x)):
				return False
		return True

	def checkQuadrant(this, q):
		quad = this.getQuadrant(q)
		exists = set()
		for val in quad:
			if val in exists and val != 0:
				return False
			else:
				exists.add(val)
		return True

	def checkRow(this, i):
		exists = set()
		for val in this.board[i]:
			if val in exists and val != 0:
				return False
			else:
				exists.add(val)
		return True

	def checkColumn(this, j):
		exists = set()
		for i in this.board:
			if i[j] in exists and i[j] != 0:
				return False
			else:
				exists.add(i[j])
		return True

	def getQuadrant(this, q):
		quad = []
		d = { 0: ((0,0),(2,2)),
			  1: ((0,3),(2,5)),
			  2: ((0,6),(2,8)),
			  3: ((3,0),(5,2)),
			  4: ((3,3),(5,5)),
			  5: ((3,6),(5,8)),
			  6: ((6,0),(8,2)),
			  7: ((6,3),(8,5)),
			  8: ((6,6),(8,8))
		}
		p1 = d[q][0]
		p2 = d[q][1]
		for i in range(p1[0], p2[0]+1):
			for j in range(p1[1], p2[1]+1):
				quad.append(this.board[i][j])
		return quad

	def getUnassigned(this):
		'''# Heuristic = Most Constrained Variable
		mostConstrained = ()
		maxConstrained = -1
		exists = set()
		for ini,i in enumerate(this.board): # row
			for inj,j in enumerate(i): # column
				if j == 0:
					c = this.getConstrained(ini,inj)
					if c and c > maxConstrained:
						maxConstrained = c
						mostConstrained = (ini,inj)
		if maxConstrained != -1:
			return mostConstrained
		else:
			return'''

		# GENERIC NEXT VARIABLE
		for ini,i in enumerate(this.board): # row
			for inj,j in enumerate(i): # column
				if j == 0:
					return (ini,inj)
		return

	def getConstrained(this, i, j):
		quad = this.getQuadrant(this.findQuadrant(i,j))
		exists = set()
		for val in this.board[i]:
			if not val in exists:
				exists.add(val)
			else:
				return
		for row in this.board:
			if not row[j] in exists:
				exists.add(row[j])
			else:
				return
		for val in quad:
			if not val in exists:
				exists.add(val)
			else:
				return
		return len(exists)

	def findQuadrant(this, i, j):
		if i <= 2: # quad 0,1,2
			if j <= 2: # q0
				return 0
			elif 2 < j <= 5: # q1
				return 1
			elif 5 < j <= 8: # q2
				return 2
		elif 2 < i <= 5: # quad 3,4,5
			if j <= 2: # q3
				return 3
			elif 2 < j <= 5: # q4
				return 4
			elif 5 < j <= 8: # q5
				return 5
		elif 5 < i <= 8: # quad 6,7,8
			if j <= 2: # q6
				return 6
			elif 2 < j <= 5: # q7
				return 7
			elif 5 < j <= 8: # q8
				return 8
		return

def solveBoard(board):
	if not board:
		return
	b = board.getBoard()
	# format check
	if(len(b) != 9):
		return
	# solve by backtracking algorithm
	board = backtracking(board)
	return board

def backtracking(board):
	if not board:
		return
	var = board.getUnassigned()
	if not var:
		return board
	for val in range(1,10):
		board.editBoard(var, val)
		#board.printBoard(); #print()
		if board.checkBoard():
			result = backtracking(board)
			if result and result.checkBoard():
				return board
		board.editBoard(var, 0)
	return
	
def TextBox(string, font):
	surface = font.render(string, True, (0,0,0))
	return surface, surface.get_rect()

def createButton(text,x,y,width,height,color1,color2):
	mPos = pygame.mouse.get_pos()
	mPressed = pygame.mouse.get_pressed()
	if x < mPos[0] < x+width and y < mPos[1] < y+width:
		pygame.draw.rect(screen, color2, (x,y,width,height))
		if mPressed[0] == 1:
			return True
	else:
		pygame.draw.rect(screen, color1, (x,y,width,height))
	writing = pygame.font.Font("freesansbold.ttf",16)
	startSurface, startRect = TextBox(text, writing)
	startRect = ((x+(width/4)),(y+(height/2)))
	screen.blit(startSurface, startRect)

def createFrame(x,y,width,height,color):
	pygame.draw.rect(screen, color, (x,y,width,height))
	writing = pygame.font.Font("freesansbold.ttf",16)
	startSurface, startRect = TextBox("", writing)
	startRect = ((x+(width/4)),(y+(height/2)))
	screen.blit(startSurface, startRect)

def constructDisplay(board = Board()):
	running = True
	solve = False
	solved = False

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False;
				return

		screen.fill((255,255,255))
		# Solve button
		solve = createButton("Solve",150, 545, 100, 50, (0,125,0), (50,100,0))
		# Quit button
		running = not createButton("Quit",550, 545, 100, 50, (225,50,0), (255,25,0))
		# Frame
		createFrame(5,5,790,535,(0,0,0))

		if solve:
			board = solveBoard(board)
			solved = True
			if not board:
				solved = False
				print("No solution.")

		board.printBoard()
		#if solved:
		#	board.printBoard()

		pygame.display.update()

def main():

	constructDisplay()
	#board = solveBoard(Board())
	#board.printBoardText()

if __name__ == '__main__':
	main()