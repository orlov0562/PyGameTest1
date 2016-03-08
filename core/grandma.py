# -*- coding: utf-8 -*-

import pygame
import random
import time

class Grandma:
	width = 64
	height = 64
	coord = [0,0]
	road = None
	bitmap = None
	died = False

	def __init__(self, road):
		self.road = road
		self.bitmap = pygame.image.load('resources/grandma%d.gif' % random.randint(1,2))
		self.coord = [
			64 + self.width + random.randint(1, road.width-self.width*3-64),
			64 + self.height + random.randint(1, road.height-self.height*3-128),
		]

		self.direction = [random.randint(-1,1),random.randint(-1,1)]
		if self.direction[0]==0 and self.direction[1]==0: self.direction[random.randint(0,1)]=1
		self.speed = random.randint(1,5)


	def draw(self, source):
		if not self.died: self.move()
		surface = pygame.Surface((self.width, self.height))
		surface.blit(self.bitmap,(0,0));

		surface.set_colorkey((0,0,0))
		source.blit(surface, (self.coord[0],self.coord[1]))

	def die(self, type):
		self.died = True
		self.bitmap = pygame.image.load('resources/die.gif')
		pygame.mixer.init()
		if type==1:
			sound = pygame.mixer.Sound('resources/shmyak.wav')
		else:
			sound = pygame.mixer.Sound('resources/scream.wav')
		sound.play()

	def setCoordOffset(self,x,y):
		self.coord[0] += x
		if self.coord[0]<0: self.coord[0] = 0
		if self.coord[0]>(self.road.width-self.width): self.coord[0] = self.road.width - self.width

		self.coord[1] += y
		if self.coord[1]<0: self.coord[1] = 0
		if self.coord[1]>(self.road.height-self.height): self.coord[1] = self.road.height - self.height

	def underCar(self,car):
		if self.died: return False

		x1 = car.coord[0] - car.width/2
		x2 = car.coord[0] + car.width/2

		y1 = car.coord[1] - car.height/2
		y2 = car.coord[1] + car.height/2

		if self.coord[0] > x1 and self.coord[0] < x2 and self.coord[1] > y1 and self.coord[1] < y2 :
			return True

		return False

	def move(self):

		self.coord[0] += self.direction[0] * self.speed
		self.coord[1] += self.direction[1] * self.speed

		if self.coord[0] > (self.road.width - 128):
				self.coord[0] = (self.road.width - 128)
				self.direction[0] *= -1
				self.direction[1] = random.randint(-1,1)

		if self.coord[1] > (self.road.height - 128):
				self.coord[1] = (self.road.height - 128)
				self.direction[1] *= -1
				self.direction[0] = random.randint(-1,1)

		if self.coord[0] < 64:
			self.coord[0] = 64
			self.direction[0] *= -1
			self.direction[1] = random.randint(-1,1)

		if self.coord[1] < 64:
			self.coord[1] = 64
			self.direction[1] *= -1
			self.direction[0] = random.randint(-1,1)

	def underRocket(self,car):
		if self.died: return False
		w = 0;
		h = 0;
		if car.rocket_direction[0]==0 and car.rocket_direction[1]==1:		# bottom
			w = car.rocket_sz[0]
			h = car.rocket_sz[1]
		elif car.rocket_direction[0]==0 and car.rocket_direction[1]==-1:	# top
			w = car.rocket_sz[0]
			h = car.rocket_sz[1]
		elif car.rocket_direction[0]==1 and car.rocket_direction[1]==0:		# right
			w = car.rocket_sz[1]
			h = car.rocket_sz[0]
		elif car.rocket_direction[0]==-1 and car.rocket_direction[1]==0:	#left
			w = car.rocket_sz[1]
			h = car.rocket_sz[0]
		else:
			if (car.rocket_sz[0]>car.rocket_sz[1]):
				w = car.rocket_sz[0]
				h = car.rocket_sz[0]
			else:
				w = car.rocket_sz[1]
				h = car.rocket_sz[1]

		x1 = car.rocket_coord[0] - w/2
		x2 = car.rocket_coord[0] + w/2

		y1 = car.rocket_coord[1] - h/2
		y2 = car.rocket_coord[1] + h/2

		if self.coord[0] > x1 and self.coord[0] < x2 and self.coord[1] > y1 and self.coord[1] < y2 :
			return True

		return False
