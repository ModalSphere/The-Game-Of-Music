import pygame, sys
from pygame.locals import *


WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700


BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (127,127,127)

def main():
	global windowSurface
	pygame.init()

	windowSurface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH), 0, 32)
	pygame.display.set_caption("Conway's Game of Music")


	basicFont = pygame.font.SysFont(None, 48)
	windowSurface.fill(WHITE)

	drawGrid()
	pygame.display.update()

	while True:
	    for event in pygame.event.get():
	    	if event.type == QUIT:
	    		pygame.quit()
	    		sys.exit()

	    pygame.display.update()


def drawGrid():
	for x in range(0,700,20):
		pygame.draw.line(windowSurface, GREY, [x,0], [x,700], 1)
	for y in range(0,700,20):
		pygame.draw.line(windowSurface,GREY,[0,y], [700,y], 1)



if __name__ == '__main__':
	main()










