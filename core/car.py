# -*- coding: utf-8 -*-

import pygame

class Car:
	width = 72
	height = 150
	coord = [0,0,0]
	road = None
	move = False
	speed = 0
	speed_inc = 1
	max_speed = 100
	speed_mult = 10
	direction = [0,0,0]
	last_direction = [0,0,0]
	bitmap = None
	shoot = False
	rocket_coord = [-1,-1]
	rocket_direction = [0,0,0]
	rocket_bitmap = None
	rocket_speed = 15
	rocket_sz = [72,32]
	explosion_bitmap = None
	shoot_explode = [0,0,0]
	died = False

	def __init__(self, road):
		self.road = road
		self.bitmap = pygame.image.load('resources/car.gif')
		self.rocket_bitmap = pygame.image.load('resources/rocket.gif')
		self.explosion_bitmap = pygame.image.load('resources/explosion.gif')
		self.coord = [road.width/2, road.height - self.height, 0]
		self.rocket_coord = self.coord
		self.rocket_direction = [0,-1,0]


	def draw(self, source):


		#pygame.draw.lines(source,(0xEE,0x00,0x00),False,[self.coord[:2],(self.coord[0],self.road.height)],1)  # redraw the points

		if self.move:
			if not pygame.mixer.music.get_busy():
				pygame.mixer.music.load('resources/engine.wav')
				pygame.mixer.music.play(-1, 0.0)

			self.speed += self.speed_inc
			if self.speed>self.max_speed: self.speed = self.max_speed
			speed = self.speed / self.speed_mult
			if speed<1: speed = 1
			self.setCoordOffset(self.direction[0] * speed, self.direction[1] * speed)
		elif self.speed>0:
			dec = 1.0 * self.speed*1/100
			if (dec<1): dec = 1
			self.speed -= dec
			if self.speed<0 or self.speed<self.speed_mult:
				if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
				self.speed=0
			speed = self.speed / self.speed_mult
			self.setCoordOffset(self.last_direction[0] * speed, self.last_direction[1] * speed)


		surface = pygame.Surface((self.width, self.height))
		surface.blit(self.bitmap,(0,0));

		#~ if (abs(abs(self.coord[2]) - abs(self.direction[2]))<90):

			#~ if (self.coord[2]<self.direction[2]):
				#~ self.coord[2] += 1
				#~ if (self.coord[2]>self.direction[2]): self.coord[2] = self.direction[2]
			#~ elif (self.coord[2]>self.direction[2]):
				#~ self.coord[2] -= 1
				#~ if (self.coord[2]<self.direction[2]): self.coord[2] = self.direction[2]
		#~ else:
		self.coord[2] = self.direction[2]

		surface = pygame.transform.rotate(surface, self.coord[2])
		surface.set_colorkey((0x0,0x0,0x0))
		source.blit(surface, (self.coord[0],self.coord[1]))

		if self.shoot:
			self.rocket_coord[0] += self.rocket_direction[0] * self.rocket_speed
			self.rocket_coord[1] += self.rocket_direction[1] * self.rocket_speed

			rocket_surface = pygame.Surface((self.rocket_sz[0],self.rocket_sz[1]))

			rocket_surface.blit(self.rocket_bitmap,(0,0));
			rocket_surface = pygame.transform.rotate(rocket_surface, self.rocket_direction[2])
			rocket_surface.set_colorkey((0x0,0x0,0x0))



			if (self.rocket_coord[0]<64) or (self.rocket_coord[1]<64):
				source.blit(self.explosion_bitmap,(self.rocket_coord[0]-64,self.rocket_coord[1]-64));
			elif (self.rocket_coord[0]>(self.road.width-128)) or (self.rocket_coord[1]>(self.road.height-128)):
				source.blit(self.explosion_bitmap,(self.rocket_coord[0],self.rocket_coord[1]));
			else:
				source.blit(rocket_surface, (self.rocket_coord[0], self.rocket_coord[1]))

			if (self.rocket_coord[0]<0) or (self.rocket_coord[1]<0) \
			or (self.rocket_coord[0]>self.road.width) or (self.rocket_coord[1]>self.road.height):
				self.shoot = False
				pygame.mixer.init()
				sound = pygame.mixer.Sound('resources/explosion.wav')
				sound.play()

		elif self.shoot_explode[2]>0:
			self.shoot_explode[2]-=1
			source.blit(self.explosion_bitmap,(self.shoot_explode[0],self.shoot_explode[1]));

	def rocketExplode(self,coord):
		rX = coord[0]-32;
		rY = coord[1]-32;

		self.shoot_explode = [rX, rY, 25]
		self.shoot = False
		self.rocket_coord = [-1,-1]

		pygame.mixer.init()
		sound = pygame.mixer.Sound('resources/explosion.wav')
		sound.play()




	def setCoordOffset(self,x,y):
		self.coord[0] += x
		if self.coord[0]<64: self.coord[0] = 64
		if self.coord[0]>(self.road.width-self.width-64): self.coord[0] = self.road.width - self.width - 64

		self.coord[1] += y
		if self.coord[1]<64: self.coord[1] = 64
		if self.coord[1]>(self.road.height-self.height-64): self.coord[1] = self.road.height - self.height - 64

	# usage example:
	# if (e.type == pygame.KEYDOWN): car.moveByKey(e.key, 25)
	def moveByKey(self, key):
		if key == pygame.K_LEFT: self.setCoordOffset(-1*step, 0)
		elif key == pygame.K_RIGHT: self.setCoordOffset(1*step, 0)
		elif key == pygame.K_UP: self.setCoordOffset(0, -1*step)
		elif key == pygame.K_DOWN: self.setCoordOffset(0, 1*step)

	def moveEvent(self):
		keys = pygame.key.get_pressed()
		self.direction[0] = 0
		self.direction[1] = 0

		if keys[pygame.K_UP]:
			self.move = True
			self.direction[1] = -1
			self.direction[2] = 0

		if keys[pygame.K_DOWN]:
			self.move = True
			self.direction[1] = 1
			self.direction[2] = 180

		if keys[pygame.K_LEFT]:
			self.move = True
			self.direction[0] = -1

			if keys[pygame.K_UP]: self.direction[2] =  45
			elif keys[pygame.K_DOWN]: self.direction[2] = 180 - 45
			else: self.direction[2] = 90

		if keys[pygame.K_RIGHT]:
			self.move = True
			self.direction[0] = 1
			if keys[pygame.K_UP]: self.direction[2] =  -90 + 45
			elif keys[pygame.K_DOWN]: self.direction[2] = 180 + 45
			else: self.direction[2] = -90

		if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
			self.move = False

		if self.move and ((self.direction[0]!=0) or (self.direction[1]!=0)):
			self.last_direction = list(self.direction)


		if keys[pygame.K_SPACE]:
			if not self.shoot:
				self.shoot = True
				rX = self.coord[0]
				rY = self.coord[1]
				if self.last_direction[0] == 1:		#right
					rX+=self.height
				elif self.last_direction[0] == -1:	#left
					rX-=self.rocket_sz[1]

				if self.last_direction[1] == 1:		#bottom
					rY+=self.height
				if self.last_direction[1] == -1:	#top
					rY-=self.rocket_sz[1]

				if self.last_direction[0] == 1 and self.last_direction[1] == -1:
					rY-=self.rocket_sz[1]

				if self.last_direction[1] == 1 and self.last_direction[0] == -1:
					rY-=self.rocket_sz[1]

				self.rocket_coord = [rX, rY]
				if self.last_direction[0] or self.last_direction[1]:
					self.rocket_direction = self.last_direction

				pygame.mixer.init()
				sound = pygame.mixer.Sound('resources/shot.wav')
				sound.play()



