import pygame
from settings import *
from pygame.math import Vector2 as vector
from math import sin, cos, tan, radians, atan2, degrees, sqrt
from debug import debug

class Block(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
		self.image = pygame.Surface((BLOCK_SIZE,BLOCK_SIZE))
		self.image.fill('black')
		self.rect = self.image.get_rect(topleft = pos)

class Monster(pygame.sprite.Sprite):
	def __init__(self, pos, group, player):
		super().__init__(group)
		self.base_image = pygame.image.load('../graphics/monster.png').convert_alpha()
		self.image = self.base_image.copy()
		self.rect = self.image.get_rect(center = (pos[0], WINDOW_HEIGHT / 2 + 50))
		self.player = player
		
		self.aspect_ratio = self.rect.width / self.rect.height

		self.font = pygame.font.Font(None, 40)

		self.max_size = 2000
		self.display_surface = pygame.display.get_surface()

	def update_size(self):
		distance_to_player = vector(self.rect.center).distance_to(self.player.pos)

		relative_size = vector(self.base_image.get_size()) / (distance_to_player * 0.0005)
		self.image = pygame.transform.scale(self.base_image, relative_size)
		self.rect = self.image.get_rect(center = self.rect.center)

	def update_pos(self):
		x_distance = self.player.rect.centerx - self.rect.centerx
		y_distance = self.player.rect.centery - self.rect.centery
		
		distance_to_player = sqrt(x_distance ** 2 + y_distance ** 2) # vector(self.rect.center).distance_to(self.player.pos) no clue why different :(
		theta = atan2(y_distance, x_distance) # angle from sprite to player 
		gamma = theta - self.player.angle # relative angle between player center view and the sprite 
		
		# debug(degrees(gamma))
		pygame.draw.line(self.display_surface,'red', self.rect.center, self.player.rect.center, 5)

		pygame.draw.line(self.display_surface,'blue', (self.rect.centerx,self.rect.centery),(self.rect.centerx + x_distance,self.rect.centery),5)
		pygame.draw.line(self.display_surface,'green', (self.rect.centerx + x_distance,self.rect.centery),(self.rect.centerx  + x_distance,self.rect.centery + y_distance),5)
		
		angle_to_player = atan2(y_distance, x_distance)

	def update(self,dt):
		self.update_size()
		self.update_pos()