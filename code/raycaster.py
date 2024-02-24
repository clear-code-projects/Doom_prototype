import pygame 
from pygame.math import Vector2 as vector
from settings import *
from math import sin, cos, tan, sqrt, degrees

from debug import debug

import numba as nb
import numpy as np 

class Raycaster:
	def __init__(self, player, collision_sprites):
		
		# general
		self.display_surface = pygame.display.get_surface()
		self.player = player
		self.walls = set([sprite.rect.topleft for sprite in collision_sprites])
		self.walls2 = nb.typed.List([sprite.rect.topleft for sprite in collision_sprites])
		

		# debug 
		self.font = pygame.font.Font(None, 30)

		# raycasting
		self.fov = 1 # basically same as pi / 3 
		self.num_rays = 400# int(WINDOW_WIDTH / 2) # 640
		self.delta_angle = self.fov / self.num_rays
		self.max_depth_cells = 20
		
		# walls 
		self.wall_width = (WINDOW_WIDTH // self.num_rays)
		self.max_wall_height = 1500 * BLOCK_SIZE
		self.window_scale = WINDOW_WIDTH / (self.num_rays * self.wall_width)

		# graphics
		self.wall_surf = pygame.image.load('../graphics/wall3.png').convert_alpha()
		self.wall_dark_surf = pygame.image.load('../graphics/wall4.png').convert_alpha()

	def draw_unoptimized(self):
		current_angle = self.player.angle - self.fov / 2 # split viewing cone in half for each side
		
		# check all rays 
		for ray in range(self.num_rays):
			sin_a = sin(current_angle)
			cos_a = cos(current_angle)
			
			# go through the full length of each array
			for depth in range(self.max_depth):
				x = self.player.rect.centerx + depth * cos_a
				y = self.player.rect.centery + depth * sin_a
				# pygame.draw.circle(self.display_surface, 'yellow',(x,y), 1) # draw the lines
 
				# check if ray is intersecting 
				if (x // BLOCK_SIZE * BLOCK_SIZE, y // BLOCK_SIZE * BLOCK_SIZE) in self.walls: # collision with grid 
					# pygame.draw.circle(self.display_surface, 'green',(x,y), 4) # draw the lines
					break
			current_angle += self.delta_angle

	def raycast_find_nearest(self, angle):
			sin_a = sin(angle)
			cos_a = cos(angle)
			tan_a = tan(angle)
			nearest_point = None
			side = None

			# column collisions -> y
			if cos_a >= 0: 
				dir_col = 1  
				start_col = (self.player.rect.centerx // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE 
			else:
				dir_col = -1
				start_col = (self.player.rect.centerx // BLOCK_SIZE) * BLOCK_SIZE 

			for step_size in range(0, BLOCK_SIZE * self.max_depth_cells, BLOCK_SIZE):
				col = start_col + step_size * dir_col

				adjacent = col - self.player.rect.centerx
				opposite = tan_a * adjacent
				y = int(self.player.rect.centery + opposite)

				cell_col = col if dir_col > 0 else col - BLOCK_SIZE
				cell_row = ((self.player.rect.centery + opposite) // BLOCK_SIZE) * BLOCK_SIZE

				if (int(cell_col), int(cell_row)) in self.walls:
					hypothenus = adjacent / cos_a
					side = 'right' if dir_col == 1 else 'left'
					nearest_point = (y, hypothenus, side)
					break
	
			# row collisions -> x
			if sin_a <= 0: 
				dir_row = -1  
				start_row = (self.player.rect.centery // BLOCK_SIZE) * BLOCK_SIZE 
			else:
				dir_row = 1
				start_row = (self.player.rect.centery // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE 

			for step_size in range(0, BLOCK_SIZE * self.max_depth_cells, BLOCK_SIZE):
				row = start_row + step_size * dir_row			
				opposite = row - self.player.rect.centery
				adjacent = opposite / tan_a
				x = int(self.player.rect.centerx + adjacent)

				cell_col = ((self.player.rect.centerx + adjacent) // BLOCK_SIZE) * BLOCK_SIZE
				cell_row = row if dir_row > 0 else row - BLOCK_SIZE
				
				if (int(cell_col), int(cell_row)) in self.walls:
					hypothenus = adjacent / cos_a
					side = 'top' if dir_row == 1 else 'bottom'
					if not nearest_point:
						nearest_point = (x,hypothenus, side)
					elif hypothenus < nearest_point[1]:
						nearest_point = (x,hypothenus, side)
					break

			# return values 
			return nearest_point

	def draw_wall_segment(self, depth, ray_index, pos, angle,side):
		# wall drawing 
			depth *= cos(self.player.angle - angle)
			wall_height = self.max_wall_height / depth

			# colors 
			c = 255 / (1 + depth * 0.005) 
			color = (c,c,c)
			
			# rect
			left = ray_index * self.wall_width
			top = (WINDOW_HEIGHT / 2) - (wall_height / 2)
			width = self.wall_width
			height = wall_height
			rect = pygame.Rect(left,top,width,height)

			# graphics
			offset = pos % BLOCK_SIZE
			selection_rect = pygame.Rect(offset * self.wall_surf.get_width() / BLOCK_SIZE,0,self.wall_width,self.wall_surf.get_height())
			wall_column = self.wall_dark_surf.subsurface(selection_rect) if side in ('right', 'top') else self.wall_surf.subsurface(selection_rect)
			wall_column = pygame.transform.scale(wall_column,rect.size)
			self.display_surface.blit(wall_column, (left,top))

			# distance shading -> needs better numbers but general logic works
			# distance_shade = wall_column.copy()
			# depth_color = 50 / (1 + depth * 0.005)
			# depth_color = min(100,max(0,depth_color))
			# distance_shade.fill((depth_color,depth_color,depth_color,150))
			# self.display_surface.blit(distance_shade, (left,top))

	def floor_cast(self):
		pass

	def draw(self):
		angles = (self.player.angle - self.fov / 2 + ray * self.delta_angle for ray in range(self.num_rays))
		for ray_index, current_angle in enumerate(angles):
			pos, depth, side = self.raycast_find_nearest(current_angle)
			if pos and depth:
				self.draw_wall_segment(depth, ray_index, pos, current_angle, side)
		debug(cos(self.player.angle))