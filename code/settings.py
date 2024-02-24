# General
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BLOCK_SIZE = 100

# Raycasting 
FOV = 1
NUM_RAYS = int(WINDOW_WIDTH / 2)
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH_CELLS = 20

# drawing
WALL_WIDTH = int(WINDOW_WIDTH / NUM_RAYS)
MAX_WALL_HEIGHT = int(FOV / NUM_RAYS)

# Level
LEVEL_MAP = [
	'xxxxxxxxxxxxxxxxxxx',
	'x        x        x',
	'xxxx             xx',
	'x     x   p  x    x',
	'x                 x',
	'x  m              x',
	'x                 x',
	'x                 x',
	'x                 x',
	'xxxxxxxxxxxxxxxxxxx',
] 
