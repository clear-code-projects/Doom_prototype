import pygame 
from settings import *
from math import degrees

class SkyBox:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.sky =  pygame.image.load('../graphics/skybox.jpg').convert()
		self.sky_width = self.sky.get_width()

	def display(self, angle_rad):
		angle = degrees(angle_rad) % 360
		self.display_surface.blit(self.sky, (angle * (self.sky_width / 360),0))
		self.display_surface.blit(self.sky, (angle * (self.sky_width / 360) - self.sky_width,0))
		
