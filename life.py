'''
Philfred's Game of Music 
Author: William Lynch

Description: takes a musical spin on the classic Game of Life, using the grid as a piano roll to output midi information.
This output can be routed to any software synthesizer running on your computer.

User Input:
- SPACE to pause and play the game
- M to toggle the music
- C to clear the grid
- MOUSE click on grid cells when paused to set them alive
'''

import pygame, sys
from pygame.locals import *
from pygame import midi

# pygame constants
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700

SQUARE_SIZE = 20

VERT_SQUARES = WINDOW_WIDTH/SQUARE_SIZE
HOR_SQUARES = VERT_SQUARES

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (127,127,127)
GREEN = (0,200,50)


# list structures to represent musical scales
SCALE1 = ["C0", "D0", "E0", "G0", "A0", "C1", "D1", "E1", "G1", "A1", "C2", "D2", "E2", "G2", "A2", "C3", "D3", "E3", "G3", "A3", "C4", "D4", "E4", "G4", "A4", "C5", "D5", "E5", "G5", "A5", "C6", "D6", "E6", "G6", "A6"]

# note name to midi numbering mapping
NOTE_MAP = {}
counter = 36
pattern = [2,2,3,2,3]
n = 0
for i in SCALE1:
	NOTE_MAP[i] = counter
	counter = counter + pattern[n%5]
	n +=1;
	
class GridSquare:
	def switch(self):
		state = not state
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.state = False


def main():
	global windowSurface, grid, instrument

	pygame.init()
	pygame.midi.init()

	for x in range( 0, pygame.midi.get_count() ):
		print pygame.midi.get_device_info(x)

	# 2d grid initialized with GridSquare objects with x and y coordinates
	grid = {(x, y): GridSquare(x,y) for x in range(HOR_SQUARES) for y in range(VERT_SQUARES)}
	instrument = pygame.midi.Output(2)

	windowSurface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), 0, 32)
	pygame.display.set_caption("Philfred's Game of Music")

	basicFont = pygame.font.SysFont(None, 48)
	windowSurface.fill(WHITE)

	drawGridLines()
	pygame.display.update()
	
	drawGrid()
	pygame.display.update()

	runGame = False
	music = False
	while True:
		drawGrid()
		pygame.display.update()
		# user event handling
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.midi.quit()
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONUP:
				xpos = event.pos[0]/SQUARE_SIZE
				ypos = event.pos[1]/SQUARE_SIZE
				grid[(xpos,ypos)].state = not grid[(xpos,ypos)].state
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					runGame = not runGame
				if event.key == K_c:
					clearGrid()
				if event.key == K_m:
					music = not music

		if runGame == True:
			grid = updateGrid()
			drawGrid()
			pygame.display.update()
			if not music:
				pygame.time.wait(300)
			if music == True:
				runMusic()

# iterates through grid columns, outputting midi information for each alive cell before moving to next column
def runMusic():
	for x in range(0,HOR_SQUARES):
		played = False
		for y in range(0,VERT_SQUARES):
			if grid[(x,y)].state == True:
				instrument.note_on(NOTE_MAP[SCALE1[y]], velocity=127, channel = 0)
				played = True
				X = x*SQUARE_SIZE+1
				Y = y*SQUARE_SIZE+1
				pygame.draw.rect(windowSurface, GREEN, (X,Y,19,19))

		

		if played == True:
			pygame.time.wait(100)
			pygame.display.update()

		for y in range(0,VERT_SQUARES):
			if grid[(x,y)].state == True:
				instrument.note_off(NOTE_MAP[SCALE1[y]], velocity=127, channel = 0)
				X = x*SQUARE_SIZE+1
				Y = y*SQUARE_SIZE+1
				pygame.draw.rect(windowSurface, GREEN, (X,Y,19,19))

		pygame.display.update()

	return 	

# kills cells if more than three or less than two neighbours alive, births dead cells with 2 neighbours
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

# kills all cells, and paints white
def clearGrid():
	for x in range(0,HOR_SQUARES):
		for y in range(0,VERT_SQUARES):
			grid[(x,y)].state = False
	updateGrid()

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

#paints cells black if alive, white if dead
def drawGrid():
	for x in range(0,VERT_SQUARES):
		for y in range(0,HOR_SQUARES):
			X = x*SQUARE_SIZE+1
			Y = y*SQUARE_SIZE+1
			if grid[(x,y)].state == True:
				pygame.draw.rect(windowSurface, BLACK, (X,Y,19,19))
			else:
				pygame.draw.rect(windowSurface, WHITE, (X,Y,19,19))

if __name__ == '__main__':
	main()










