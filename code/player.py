import pygame
from settings import *
from pygame.math import Vector2 as vector
from math import sin, cos
from debug import debug

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites):
		
		# general setup
		self.display_surface = pygame.display.get_surface()
		super().__init__(group)
		
		# sprite
		self.image = pygame.Surface((60,60))
		self.image.fill('white')
		self.rect = self.image.get_rect(topleft = pos)

		# movement
		self.pos = vector(self.rect.topleft)
		self.direction = vector()
		self.speed = 300
		self.collision_sprites = collision_sprites
		
		# view
		self.angle = 0
		self.range = 200

		# raycaster center 
		self.x = int(self.rect.centerx)
		self.y = int(self.rect.centery)

	def input(self, dt):
		
		# simple movement / topdown
		# if keys[pygame.K_w]:
		# 	self.direction.y = -1
		# elif keys[pygame.K_s]:
		# 	self.direction.y = 1
		# else:
		# 	self.direction.y = 0

		# if keys[pygame.K_a]:
		# 	self.direction.x = -1
		# elif keys[pygame.K_d]:
		# 	self.direction.x = 1
		# else:
		# 	self.direction.x = 0

		# proper movement / FPS
		dir_vector = vector()
		sin_a = sin(self.angle)
		cos_a = cos(self.angle)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			dir_vector.x += cos_a
			dir_vector.y += sin_a
		if keys[pygame.K_s]:
			dir_vector.x -= cos_a
			dir_vector.y -= sin_a
		if keys[pygame.K_a]:
			dir_vector.y -= cos_a
			dir_vector.x += sin_a
		if keys[pygame.K_d]:
			dir_vector.y += cos_a
			dir_vector.x -= sin_a
		self.direction = dir_vector.normalize() if dir_vector.magnitude() else dir_vector
		
		if keys[pygame.K_RIGHT]:
			self.angle += 2 * dt
		if keys[pygame.K_LEFT]:
			self.angle -= 2 * dt
		self.angle = self.angle # radians! 


	# movement
	def move(self, dt):
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)
		self.collision('horizontal')

		self.pos.y += self.direction.y * self.speed * dt
		self.rect.y = round(self.pos.y)
		self.collision('vertical')
		self.update_raycaster_center()

	def update_raycaster_center(self):
		self.x = int(self.rect.centerx)
		self.y = int(self.rect.centery)

	def collision(self,direction):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.rect):
				if direction == 'horizontal':
					if self.direction.x > 0: # moving right 
						self.rect.right = sprite.rect.left
					if self.direction.x < 0: # moving left
						self.rect.left = sprite.rect.right
					self.pos.x = self.rect.x

				else: # vertical
					if self.direction.y > 0: # moving down
						self.rect.bottom = sprite.rect.top
					if self.direction.y < 0: # moving up
						self.rect.top = sprite.rect.bottom
					
					self.pos.y = self.rect.y

	# view
	def show_view(self):
		x = self.rect.centerx + self.range * cos(self.angle)
		y = self.rect.centery + self.range * sin(self.angle)
		pygame.draw.line(self.display_surface,'white',self.rect.center,(x,y),5)


	# update
	def update(self, dt):
		self.input(dt)
		self.move(dt)
		self.show_view()

		# safety 
		self.angle = 0.0001 if self.angle == 0 else self.angle