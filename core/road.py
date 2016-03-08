# -*- coding: utf-8 -*-

import pygame

class Road:
	surface = None
	bg = None
	width = 640
	height = 480
	coord = [0,0]
	items = []
	bitmap = None
	totalGrandmaDeath = 0
	totalMonsterDeath = 0
	level = 1

	def __init__(self, width, height):
		self.surface = pygame.Surface((width, height))
		self.bg = pygame.Surface((width, height))
		self.width = width
		self.height = height
		self.bitmap = pygame.image.load('resources/bg.jpg')
		self.bitmap = pygame.transform.scale(self.bitmap,(width, height))
		self.bg.blit(self.bitmap,(0,0))

	def draw(self, source):
		self.surface = self.bg.copy()
		for i in self.items:
			if i.died:
				i.draw(self.surface)

		for i in self.items:
			if not i.died:
				i.draw(self.surface)

		pygame.font.init()
		#font = pygame.font.Font(None, 32) # default font
		font = pygame.font.SysFont('Dejavu Sans', 24, True, False); # duser specified font
		self.surface.blit(font.render('Lvl: %d. Died grandmams: %d , viruses: %d' % (self.level, self.totalGrandmaDeath, self.totalMonsterDeath), 1, (0XFF,0xFF,0xFF)), (10,10))

		source.blit(self.surface, self.coord)

