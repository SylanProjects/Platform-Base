import pygame as pg

# Game Options
TITLE = 'ML Platform Game'
FPS = 30
WIDTH = 1280
HEIGHT = 960
TILESIZE = 32


# Player Properties
PLAYER_IMG = 'player.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE)
PLAYER_HEALTH = 100

PLAYER_ACC = 1
PLAYER_FRICTION = -0.20
PLAYER_JUMP = 35
PLAYER_GRAV = 1.2

PLAYER_SPEED = 280



# colors
BGCOLOR = (30, 255, 250)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

PLAYER_LAYER = 2
WALL_LAYER = 4
ITEMS_LAYER = 2
