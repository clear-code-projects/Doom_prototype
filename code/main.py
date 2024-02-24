import pygame, sys
from settings import *

from level import Level

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()

		self.level = Level()

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.level.run(dt)
			pygame.display.update()
			pygame.display.set_caption(str(round(self.clock.get_fps(),2)))

main = Main()
main.run()