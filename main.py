import pygame
from sys import exit 
from pygame import mixer


HOME_X = 400
HOME_Y = 300

# Starts pygame and initiates all sub parts of pygame
pygame.init()

# Instantiate mixer
mixer.init()

# Load audio file
mixer.music.load('music/theme.mp3')

# Play
mixer.music.play(loops= 100)
mixer.music.set_volume(0.1)

# Creating display surface
screen = pygame.display.set_mode((800,600)) 
screen.fill('White')
# Setting a title caption to our pygame window
pygame.display.set_caption("Icy Tower")

# Setting up icon 
game_icon = pygame.image.load("icons\icytowericon.png")
pygame.display.set_icon(game_icon)

# Creating clock object for time and framerate setup
clock = pygame.time.Clock()


# Setting up background image
background_surf = pygame.image.load('sprites/background.jpg').convert()

# setting up right wall
rightWall_surf = pygame.image.load('sprites/wall2.png').convert_alpha()
rightWall_surf = pygame.transform.scale(rightWall_surf,(125*(1/3),677*(1/3)))
rightWall_rect1 = rightWall_surf.get_rect(topright = (800,0))
rightWall_rect2 = rightWall_surf.get_rect(topright = (800,200))
rightWall_rect3 = rightWall_surf.get_rect(topright = (800,400))

# setting up left wall
leftWall_surf = pygame.image.load('sprites/wall2.png').convert_alpha()
leftWall_surf = pygame.transform.scale(leftWall_surf,(125*(1/3),677*(1/3)))
leftWall_surf = pygame.transform.rotate(leftWall_surf,180)
leftWall_rect1 = leftWall_surf.get_rect(topleft = (0,0))
leftWall_rect2 = leftWall_surf.get_rect(topleft = (0,200))
leftWall_rect3 = leftWall_surf.get_rect(topleft = (0,400))

# Setting up the character
PLAYER_X = 208/6.5
PLAYER_Y = 411/6.5
PLAYER_GRAVITY = 0
player_surf = pygame.image.load('sprites/icyMan.png')
player_surf = pygame.transform.scale(player_surf, (PLAYER_X, PLAYER_Y))
player_rect = player_surf.get_rect(midbottom = (100,600))


# font
test_font = pygame.font.Font('fonts/agency_fb.ttf', 50)

# Gameloop
while True :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    screen.blit(background_surf,(0,0))
    screen.blit(rightWall_surf,rightWall_rect1)
    screen.blit(rightWall_surf,rightWall_rect2)
    screen.blit(rightWall_surf,rightWall_rect3)
    
    screen.blit(leftWall_surf,leftWall_rect1)
    screen.blit(leftWall_surf,leftWall_rect2)
    screen.blit(leftWall_surf,leftWall_rect3)


    PLAYER_GRAVITY += 0.7
    player_rect.y += PLAYER_GRAVITY   
    if player_rect.bottom >= 600:
        player_rect.bottom = 600
        PLAYER_GRAVITY = 0
    
    screen.blit(player_surf,player_rect)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        # player_rect.move(PLAYER_X-10,PLAYER_Y)
        player_rect.x-=7
    if keys[pygame.K_RIGHT]:
        # player_rect.move(PLAYER_X+10,PLAYER_Y)
        player_rect.x+=7
    if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        PLAYER_GRAVITY = -10
    
    pygame.display.update() 
    clock.tick(60) 