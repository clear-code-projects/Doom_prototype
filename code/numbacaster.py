import pygame 
from pygame.math import Vector2 as vector
from settings import *
from math import sin, cos, tan, sqrt, degrees

from debug import debug

import numba as nb
import numpy as np 

class NumbaCaster:
	def __init__(self, player, collision_sprites):
		self.display_surface = pygame.display.get_surface()
		self.player = player
		self.walls = nb.typed.List([sprite.rect.topleft for sprite in collision_sprites])

		# raycasting
		self.fov = 1 # basically same as pi / 3 
		self.num_rays =  10 # int(WINDOW_WIDTH / 2) # 640
		self.delta_angle = self.fov / self.num_rays
		self.max_depth = 20

		# numba 
		columns = 3
		self.point_array = np.zeros(self.num_rays * columns).reshape(self.num_rays,columns)

	def draw_points(self):
		# self.point_array = self.get_points(
		# 	player_x = self.player.x, player_y = self.player.y, angle = self.player.angle, fov = self.fov, 
		# 	num_rays = self.num_rays, delta_angle = self.delta_angle, point_array = self.point_array, max_depth = self.max_depth, block_size = BLOCK_SIZE, 
		# 	walls = self.walls)
	
		# for point in self.point_array:
		# 	pygame.draw.line(self.display_surface, 'red', (point[0],point[1]), (self.player.x, self.player.y), 5)
		# 	pygame.draw.line(self.display_surface, 'blue', (point[3],point[4]), (self.player.x, self.player.y), 5)

		self.point_array = self.get_array(self.player.x, self.player.y, self.player.angle, self.fov, self.num_rays, self.delta_angle, self.point_array, 
			self.max_depth,BLOCK_SIZE, self.walls)
		for point in self.point_array:
			pygame.draw.line(self.display_surface, 'red', (point[0], point[1]), self.player.rect.center, 5)

	@staticmethod
	@nb.njit(fastmath = True, parallel = True)	
	def get_array(player_x, player_y, angle, fov, num_rays, delta_angle, point_array, max_depth, block_size, walls):

		angles = np.linspace(angle - fov / 2, angle + fov / 2, num_rays)
		for ray, angle in enumerate(angles):
			sin_a, cos_a, tan_a = np.sin(angle), np.cos(angle), np.tan(angle)
			
			# x/y positions for each ray
			x = player_x + 300 * cos_a
			y = player_y + 300 * sin_a
			# point_array[ray][0] = x
			# point_array[ray][1] = y
			# point_array[ray][2] = angle
			
			# column collisions -> y
			if cos_a >= 0: 
				dir_col = 1  
				start_col = (player_x // block_size) * block_size + block_size 
			else:
				dir_col = -1
				start_col = (player_x // block_size) * block_size 

			for step_size in range(0, block_size * max_depth, block_size):
				col = start_col + step_size * dir_col

				adjacent = col - player_x
				opposite = tan_a * adjacent
				y = player_y + opposite

				cell_col = col if dir_col > 0 else col - block_size
				cell_row = ((player_y + opposite) // block_size) * block_size

				if (int(cell_col), int(cell_row)) in walls:
					point_array[ray][0] = col
					point_array[ray][1] = y
					point_array[ray][2] = adjacent / cos_a # hypothenus
					break

		return point_array


	@staticmethod
	@nb.njit(fastmath = True, parallel = True)
	def get_points(player_x, player_y, angle, fov, num_rays, delta_angle, point_array, max_depth, block_size, walls):

		# current_angle = angle - fov / 2
		angles = np.linspace(angle - fov / 2, angle + fov / 2, num_rays)
		for ray, angle in enumerate(angles):
			sin_a, cos_a, tan_a = np.sin(angle), np.cos(angle), np.tan(angle)

			# column collisions -> y
			if cos_a >= 0: 
				dir_col = 1  
				start_col = (player_x // block_size) * block_size + block_size 
			else:
				dir_col = -1
				start_col = (player_x // block_size) * block_size 

			for step_size in range(0, block_size * max_depth, block_size):
				col = start_col + step_size * dir_col

				adjacent = col - player_x
				opposite = tan_a * adjacent
				y = player_y + opposite

				cell_col = col if dir_col > 0 else col - block_size
				cell_row = ((player_y + opposite) // block_size) * block_size

				if (int(cell_col), int(cell_row)) in walls:
					point_array[ray][0] = col
					point_array[ray][1] = y
					point_array[ray][2] = adjacent / cos_a # hypothenus
					break

			# row collisions -> x
			if sin_a <= 0: 
				dir_row = -1  
				start_row = (player_y // block_size) * block_size 
			else:
				dir_row = 1
				start_row = (player_y // block_size) * block_size + block_size 

			for step_size in range(0, block_size * max_depth, block_size):
				row = start_row + step_size * dir_row			
				opposite = row - player_y
				adjacent = opposite / tan_a
				x = player_x + adjacent

				cell_col = ((player_x + adjacent) // block_size) * block_size
				cell_row = row if dir_row > 0 else row - block_size
				
				if (int(cell_col), int(cell_row)) in walls:
					point_array[ray][3] = x
					point_array[ray][4] = row
					point_array[ray][5] = adjacent / cos_a # hypothenus
					break

		return point_array