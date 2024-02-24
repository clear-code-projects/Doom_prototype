import pygame 
import numpy as np
from settings import *
from numba import njit, prange 
from math import sin, cos, tan, sqrt, degrees

from numba import njit, prange

class Mode7:
	def __init__(self, player):
		
		self.display_surface = pygame.display.get_surface()
		self.player = player
		
		self.floor_surf = pygame.image.load('../graphics/floor2.png').convert()
		self.floor_size = self.floor_surf.get_size()
		self.floor_array = pygame.surfarray.array3d(self.floor_surf)
		
		self.display_array = pygame.surfarray.array3d(pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)))


	def draw(self):
		self.draw_floor_unoptimized()
		# self.display_array = self.get_floor_array(
		# 	self.floor_array, 
		# 	self.display_array, 
		# 	self.floor_size, 
		# 	self.player.x,
		# 	self.player.y)
		
		# self.display_surface.blit(self.floor_surf, (0,0))

	def draw_floor_unoptimized(self):
		for col in range(WINDOW_WIDTH):
			for row in range(WINDOW_HEIGHT // 2, WINDOW_HEIGHT):
				
				# x y z
				x = WINDOW_WIDTH / 2 - col
				y = row + 250 # focal length 
				z = row - WINDOW_HEIGHT // 2 + 0.01

				# projection
				px = x / z * 100 # scale 
				py = y / z * 100 # scale 

				# floor pixel pos and color 
				floor_pos = int(px % self.floor_size[0]), int(py % self.floor_size[1])
				floor_col = self.floor_array[floor_pos]

	 			# fill screen
				self.display_array[col,row] = floor_col
		pygame.surfarray.blit_array(self.display_surface, self.display_array)


	# @staticmethod
	# @njit(fastmath = True, parallel = True)
	# def get_floor_array(floor_array, display_array, floor_size, pos_x, pos_y):
	# 	for col in prange(WINDOW_WIDTH):
	# 		for row in range(WINDOW_HEIGHT // 2, WINDOW_HEIGHT):

	# 			# x y z
	# 			x = WINDOW_WIDTH / 2 - col
	# 			y = row + 100 # focal length 
	# 			z = row - WINDOW_HEIGHT // 2 + 0.01

	# 			# projection
	# 			px = (x / z + pos_x) * 80 # scale 
	# 			py = (y / z + pos) * 80 # scale 

	# 			# floor pixel pos and color 
	# 			floor_pos = int(px % floor_size[0]), int(py % floor_size[1])
	# 			floor_col = floor_array[floor_pos]

	# 			# fill screen
	# 			display_array[col,row] = floor_col
		
	# 	return display_array