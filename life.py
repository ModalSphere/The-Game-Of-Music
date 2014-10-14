import pygame, sys
from pygame.locals import *


WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700

SQUARE_SIZE = 20

VERT_SQUARES = WINDOW_WIDTH/SQUARE_SIZE
HOR_SQUARES = VERT_SQUARES

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (127,127,127)

class GridSquare:
	def switch(self):
		state = not state
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.state = False


def main():
	global windowSurface, grid
	pygame.init()

	grid = {(x, y): GridSquare(x,y) for x in range(HOR_SQUARES) for y in range(VERT_SQUARES)}

	windowSurface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), 0, 32)
	pygame.display.set_caption("Conway's Game of Music")


	basicFont = pygame.font.SysFont(None, 48)
	windowSurface.fill(WHITE)

	drawGridLines()
	pygame.display.update()
	
	drawGrid()
	pygame.display.update()

	runGame = False
	while True:
		drawGrid()
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONUP:
				xpos = event.pos[0]/20
				ypos = event.pos[1]/20
				grid[(xpos,ypos)].state = not grid[(xpos,ypos)].state
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					runGame = not runGame

		if runGame == True:
			grid = updateGrid()
			drawGrid()
			pygame.display.update()

			pygame.time.wait(800)


def updateGrid():
	newgrid = {}
	for x in range(0,HOR_SQUARES):
		for y in range(0,VERT_SQUARES):
			newgrid[(x,y)] = GridSquare(x,y)
			if grid[(x,y)].state == True:
				if getNeighbours(grid[(x,y)]) < 2 or getNeighbours(grid[(x,y)]) > 3:
					newgrid[(x,y)].state = False
				else:
					newgrid[(x,y)].state = True
			if grid[(x,y)].state == False:
				if getNeighbours(grid[(x,y)]) == 3:
					newgrid[(x,y)].state = True
				
	return newgrid

def getNeighbours(square):
	neighbours = 0
	for x in range(square.x-1,square.x+2):
		if x>-1 and square.y-1>-1 and x<VERT_SQUARES:
			if grid[(x,square.y-1)].state==True:
				neighbours += 1
	if square.x-1>-1:
		if grid[(square.x-1,square.y)].state == True:
			neighbours += 1
	if square.x+1<HOR_SQUARES:
		if grid[(square.x+1,square.y)].state == True:
			neighbours += 1
	for x in range (square.x-1,square.x+2):
		if x>-1 and x<VERT_SQUARES and square.y+1<VERT_SQUARES:
			if grid[(x,square.y+1)].state==True:
				neighbours += 1
	return neighbours


def drawGridLines():
	for x in range(0,700,20):
		pygame.draw.line(windowSurface, GREY, [x,0], [x,WINDOW_WIDTH], 1)
	for y in range(0,700,20):
		pygame.draw.line(windowSurface,GREY,[0,y], [WINDOW_HEIGHT,y], 1)

def drawGrid():
	for x in range(0,VERT_SQUARES):
		for y in range(0,HOR_SQUARES):
			X = x*20+1
			Y = y*20+1
			if grid[(x,y)].state == True:
				pygame.draw.rect(windowSurface, BLACK, (X,Y,19,19))
			else:
				pygame.draw.rect(windowSurface, WHITE, (X,Y,19,19))

if __name__ == '__main__':
	main()










