import pygame
import os

pygame.font.init()

TEXT_FONT = pygame.font.Font('fonts/agency_fb.ttf', 25)
PLAYER_VEL = 5
OFFSET_Y = 50
scroll = 0
PLAYER_X = 208/6.5
PLAYER_Y = 411/6.5
WIN_WIDTH = 800
WIN_HEIGHT = 600
GAME_ACTIVE = True
MAX_FLOORS = 15
FALLING = False
FLOOR_VELOCITY = 0

floor_indices = []
START_TIME = 0
floor_y = WIN_HEIGHT-150
floor_yy = WIN_HEIGHT -150
floor_group = list()
removed_floor = 0
music_dict = {
    "gameBG" : os.path. join("music","gameBG.mp3"),
    "theme" : os.path.join("music","theme.mp3"),
    "gameOverSound" : os.path.join("music","gameover.ogg"),
    "menuchoose" : os.path.join("music","menuchoose.ogg"),
    "menuchange" : os.path.join("music","menuchange.ogg"),
    "tryagain" : os.path.join("music","tryagain.ogg"),
    "hurryup" : os.path.join("music","hurryup.ogg"),
}
