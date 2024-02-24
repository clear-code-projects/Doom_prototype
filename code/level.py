import pygame
from settings import *
from sprites import Block, Monster
from player import Player
from pygame.math import Vector2 as vector

from raycaster import Raycaster
from numbacaster import NumbaCaster
from skybox import SkyBox
from mode7 import Mode7
from debug import debug

import numpy as np

class Level:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.collision_sprites = pygame.sprite.Group()
		self.all_sprites = pygame.sprite.Group()
		self.monster_sprites = pygame.sprite.Group()
		self.setup()
		
		# display 
		self.skybox = SkyBox()
		self.raycaster = Raycaster(self.player, self.collision_sprites)
		self.numbacaster = NumbaCaster(self.player, self.collision_sprites)
		self.mode7 = Mode7(self.player)

	def setup(self):
		for row_index, row in enumerate(LEVEL_MAP):
			for col_index, col in enumerate(row):
				if not col.isspace():
					pos = (col_index * BLOCK_SIZE,row_index * BLOCK_SIZE)
					if col == 'x':
						Block(pos, (self.all_sprites, self.collision_sprites))
					if col == 'p':
						self.player = Player(pos, self.all_sprites, self.collision_sprites)
					# if col == 'm':
					# 	Block(pos, (self.all_sprites, self.collision_sprites))
					# 	Monster(pos, [self.all_sprites, self.monster_sprites], self.player)

	def draw_grid(self):
		cols = len(LEVEL_MAP[0])
		rows = len(LEVEL_MAP)

		for col in range(cols):
			x = col * BLOCK_SIZE
			pygame.draw.line(self.display_surface,'white', (x,0), (x,1000))

		for row in range(rows):
			y = row * BLOCK_SIZE
			pygame.draw.line(self.display_surface,'white', (0,y), (2000,y))

	def run(self, dt):
		self.display_surface.fill('gray')
		
		# top down stuff
		self.draw_grid()
		self.all_sprites.draw(self.display_surface)
		# self.numbacaster.draw_points()
		
		# 3D
		self.all_sprites.update(dt)
		self.skybox.display(self.player.angle)
		# self.mode7.draw()
		self.raycaster.draw()


