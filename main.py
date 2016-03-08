#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
import gtk


#~ try:
    #~ import pygame_sdl2
    #~ pygame_sdl2.import_as_pygame()
#~ except ImportError:
	#~ print 'Error'
	#~ sys.exit(0)

from core.road import Road
from core.car import Car
from core.grandma import Grandma
from core.monster import Monster

# -------------------------------------------------------------------------------------
os.system('clear');
pygame.init()
# -------------------------------------------------------------------------------------
def getScreenSz():
	window = gtk.Window()
	screen = window.get_screen()

	monitors = []
	for m in range(screen.get_n_monitors()):
	  mg = screen.get_monitor_geometry(m)
	  monitors.append(mg)

	curmon = screen.get_monitor_at_window(screen.get_active_window())
	x, y, width, height = monitors[curmon]
	return {'W':width, 'H':height}

def alignWindowToCenter(screenSz):
	os.environ['SDL_VIDEO_CENTERED'] = '0'
	pos_x = screenSz['W']/2 - WINDOW['W']/2
	pos_y = screenSz['H']/2 - WINDOW['H']/2
	os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y)

def resPath(path):
	return sys.path.append(os.path.realpath(__file__))+'/'+path

# -------------------------------------------------------------------------------------

screenSz = getScreenSz()

WINDOW = {
	'W':int(screenSz['W'] - 150),
	'H':int(screenSz['H'] - 150),
	'C':'My first python game',
	'FPS': 30
}

# -------------------------------------------------------------------------------------

alignWindowToCenter(screenSz)
window = pygame.display.set_mode((WINDOW['W'],WINDOW['H']))
pygame.display.set_caption(WINDOW['C'])

# -------------------------------------------------------------------------------------

road = Road(WINDOW['W'], WINDOW['H'])

grandma = Grandma(road)
road.items.append(grandma)

car = Car(road)
road.items.append(car)

monsters = []

# -------------------------------------------------------------------------------------

def drawScene(window):
	road.draw(window)

# -------------------------------------------------------------------------------------
# pygame.key.set_repeat(1,1);

# clock ticks
# https://www.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/

end = False
clock = pygame.time.Clock()
frame = 0
startLevel = WINDOW['FPS'] * 11 # 11 per second

while not end:
	for e in pygame.event.get():
		if (e.type == pygame.QUIT): end = True
		else: car.moveEvent()

	if grandma.underCar(car):
		grandma.die(1)
		grandma = Grandma(road)
		road.items.insert(len(road.items)-1, grandma)
		road.totalGrandmaDeath += 1
		frame = 0
	elif grandma.underRocket(car):
		grandma.die(0)
		car.rocketExplode(grandma.coord)
		grandma = Grandma(road)
		road.items.insert(len(road.items)-1, grandma)
		road.totalGrandmaDeath += 1
		frame = 0

	for m in monsters:
		if not m.died and m.underRocket(car):
			m.die(0)
			car.rocketExplode(m.coord)
			road.totalMonsterDeath += 1

	#~ while (len(road.items)>50):
		#~ for i in road.items:
			#~ print road.items.index(i),') ',i
			#~ if isinstance(i, Grandma):
				#~ if i.died:
					#~ road.items.remove(i)
					#~ break;

	drawScene(window)
	#pygame.time.delay(1000 / WINDOW['FPS'])
	msElapsed = clock.tick_busy_loop(WINDOW['FPS'])
	pygame.display.flip()

	frame+=1
	road.level = road.totalGrandmaDeath/10
	if (road.level<1): road.level = 1
	monsterRegenerationSpeed = int(startLevel - road.level)
	if (monsterRegenerationSpeed<WINDOW['FPS']): monsterRegenerationSpeed = WINDOW['FPS']
	if not frame % monsterRegenerationSpeed: # increase level after 10 killed grandmams
		monster = Monster(road, grandma.coord)
		road.items.insert(len(road.items)-1, monster)
		monsters.append(monster)

