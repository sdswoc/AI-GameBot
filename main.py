import pygame
import sys
from sys import exit 
from pygame import mixer
from random import randint
import os

# Initializing pygame and mixer
pygame.init()
mixer.init()

# Constants
TEXT_FONT = pygame.font.Font('fonts/agency_fb.ttf', 50)
HOME_X = 400
HOME_Y = 300
PLAYER_X = 208/6.5
PLAYER_Y = 411/6.5
PLAYER_GRAVITY = 0
WIN_WIDTH = 800
WIN_HEIGHT = 600
GAME_ACTIVE = True
MAX_FLOORS = 200
PLAYER_THIRDWAY = False
PLAYER_2THIRDWAY = False
FLOOR_VELOCITY = 0
FLOOR_TIMER = 0


class Floor(pygame.sprite.Sprite):
    def __init__(self,x,y, width):
        self.width = width
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.imagesolid = pygame.transform.scale(floor_surf, (self.width, floor_surf.get_height()))
        self.image = floor_surf
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.rectsolid = self.imagesolid.get_rect(topleft = (self.x, self.y))
    def get_width(self):
        return self.width
    def get_x(self) : return self.x
    def get_y(self) : return self.y

def place_surface (surf,rect):
    screen.blit(surf,rect)


# Function to draw floor starting from start x location to end x location
def draw_floor(floor,rect,st,en):
    rect.x = st
    while rect.x<en:
        if PLAYER_THIRDWAY:
            rect.top += FLOOR_VELOCITY
        screen.blit(floor, rect)
        rect.x += floor.get_width()
def floor_sprite(floor_group):
    for floor in floor_group:
        floor.rect.x = floor.get_x()
        while floor.rect.x < (floor.get_x() + floor.get_width()):
            screen.blit(floor.image, floor.rect)
            floor.rect.x += floor_surf.get_width()


# Creating display surface
screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) 
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


# setting up walls
RWall_surf = pygame.transform.rotozoom(pygame.image.load('sprites/wall2.png').convert_alpha(),0,0.4)
LWall_surf = pygame.transform.flip(RWall_surf,True, False)
wallList = []
wallList.append(RWall_surf.get_rect(topright = (804,0)))
wallList.append(RWall_surf.get_rect(topright = (804,240)))
wallList.append(RWall_surf.get_rect(topright = (804,480)))
wallList.append(LWall_surf.get_rect(topright = (LWall_surf.get_width()-4,0)))
wallList.append(LWall_surf.get_rect(topright = (LWall_surf.get_width()-4,240)))
wallList.append(LWall_surf.get_rect(topright = (LWall_surf.get_width()-4,480)))


# Setting up floor
floor_surf = pygame.image.load('sprites/icy2.png').convert()                 
floor_rect = floor_surf.get_rect(topleft = (0,WIN_HEIGHT-floor_surf.get_height()))
floor_y = WIN_HEIGHT-150
floor_yy = WIN_HEIGHT -150
floor_group = pygame.sprite.Group()

for floor in range(MAX_FLOORS):
    f_w = randint(120,400)
    f_x = randint(30,WIN_WIDTH-f_w-30) 
    # print(f_x, floor_yy, f_w)
    floor = Floor(f_x, floor_yy, f_w)
    floor_group.add(floor)
    floor_yy -= 100

floor_rect_list = []

# print(screen.get_width())
# floor timer
# FLOOR_TIMER = pygame.USEREVENT + 1
# pygame.time.set_timer(FLOOR_TIMER, 1)

# setting up player
player_surf = pygame.image.load('sprites/icyMan.png')
player_surf = pygame.transform.scale(player_surf, (PLAYER_X, PLAYER_Y))
player_rect = player_surf.get_rect(midbottom = (100,WIN_HEIGHT-floor_surf.get_height()))


# Background music
mixer.Channel(0).play(mixer.Sound('music/gameBG.mp3'), loops= 100)
# mixer.Channel(1).play(mixer.Sound('music/theme.mp3'), loops= 100)
mixer.Channel(0).set_volume(0.01)
# mixer.Channel(1).set_volume(0)

jump_counter = 0

def welcome(screen):
    # WIN_HEIGHT= 900
    # WIN_WIDTH = 700
    SCREEN = screen
    pygame.display.set_caption("IcyTower")
    tilt = 0 
    turn = True
    font = TEXT_FONT
    font.bold = True
    font.italic = False
    active = True
    menu = ["PlayGame", "Instruction", "Profile", "HighScore", "LoadReplay", "Options", "Exit"]
    index = 0
    menu_dict = {
         "PlayGame" : True,
         "Instruction" : False,
         "Profile" : False,
         "HighScore" : False,
         "LoadReplay" : False,
         "Options" : False,
         "Exit" : False 
    }
    clock = pygame.time.Clock()
    temp_im = pygame.image.load(os.path.join("sprites", "icyMan.png"))
    im = pygame.transform.rotozoom(temp_im,0, 0.5)

    menu_img = pygame.image.load(os.path.join("sprites", "menu.png"))
    menu_img = pygame.transform.rotozoom(menu_img, 0, 1.3)
    menu_rect = menu_img.get_rect(center=(WIN_WIDTH//2 + 150, WIN_HEIGHT//2 + 150))

    hand_img = pygame.image.load(os.path.join("sprites", "hand.png"))
    hand_img = pygame.transform.rotozoom(hand_img, 0, 0.6)

    hand_rect = hand_img.get_rect(center=(WIN_WIDTH//2 - 18, WIN_HEIGHT//2 +  80  ))

    logo_im = pygame.image.load(os.path.join("sprites","homescreen1.png")).convert_alpha()
    logo_im = pygame.transform.rotozoom(logo_im, 0, 1.2)
    logo_rect = logo_im.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2 - 130))

    while active:
        SCREEN.fill((0,0,0))
        SCREEN.blit(background_surf, (0,0))
        SCREEN.blit(logo_im, logo_rect)
        rot_image = pygame.transform.rotate(im, tilt)
        new_rect = rot_image.get_rect(center=(WIN_WIDTH//2 - 220, WIN_HEIGHT//2 + 150))

        SCREEN.blit(rot_image, new_rect)
        SCREEN.blit(menu_img, menu_rect)
        SCREEN.blit(hand_img, hand_rect)

        if turn:
            tilt += .5
            if tilt == 40:
                turn = False
        else:
            tilt -= .5
            if tilt == -40:
                turn = True
        

        for event in pygame.event.get():
            if (event.type == pygame.QUIT)  :
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_DOWN and index<(len(menu)-1):
                    hand_rect.y += 28.5
                    menu_dict[menu[index]] = False
                    menu_dict[menu[index+1]] = True
                    index += 1
                elif event.key == pygame.K_UP and index>0:
                    hand_rect.y -= 28.5
                    menu_dict[menu[index]] = False
                    menu_dict[menu[index-1]] = True
                    index -= 1
                elif event.key == pygame.K_RETURN:
                    return menu_dict
        pygame.display.update()
        clock.tick(60)
        
    
    


menu = welcome(screen)
GAME_ACTIVE = menu["PlayGame"]
# Gameloop
while True :
    collide_left = False
    collide_right = False
    scroll = 100
    offset_y = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        # Checking collision with left wall so that player can't go out of screen
        if player_rect.left < wallList[3].right:
            collide_left = True
            # print("collided with left wall")
        else:
            player_rect.x-=5
    if keys[pygame.K_RIGHT]:
        # Checking collision with right wall so that player can't go out of screen
        if player_rect.right > wallList[0].left:
            collide_right = True
            # print("collided with right wall")
        else:
            player_rect.x+=5
    # Events loop
    for event in pygame.event.get()  :
        if event.type == pygame.QUIT or (menu["Exit"]):
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # keys = pygame.key.get_pressed()
                if player_rect.bottom <= WIN_HEIGHT+50 and jump_counter == 0 :     
                    PLAYER_GRAVITY = -13
                    jump_counter += 1
            keys = pygame.key.get_pressed()                    
            if (keys[pygame.K_SPACE]) and player_rect.bottom <= WIN_HEIGHT+50 and jump_counter == 1 and (collide_left or collide_right) and PLAYER_GRAVITY!= 0 :     
                PLAYER_GRAVITY = -15
                collide_right = False
                collide_left = False
                # player_rect.x += 100
                jump_counter += 1
    

    # Drawing Random Floors
         
    # if len(floor_rect_list) <100:
    #     start = 60
    #     end = WIN_WIDTH - 100
    #     rand_start = randint(start,end)
    #     rand_end = randint(rand_start,end)
    #     if (rand_end - rand_start) > 50 and (rand_end - rand_start) < 300 :
    #         if len(floor_rect_list) > 0 :
    #             if (floor_rect_list[-1][2] - rand_start)<100:
    #                 temp = [floor_surf.get_rect(topleft = (rand_start,floor_y)),rand_start,rand_end]
    #                 floor_rect_list.append(temp)
    #                 floor_y -= 100
    #         else:
    #             temp = [floor_surf.get_rect(topleft = (rand_start,floor_y)),rand_start,rand_end]
    #             floor_rect_list.append(temp)
    #             floor_y -= 100
    

    # User Input Handling
    
    # if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
    #     if player_rect.bottom <= WIN_HEIGHT+50 and jump_counter == 0 :     
    #         PLAYER_GRAVITY = -13
    #         jump_counter += 1
    #     elif player_rect.bottom <= WIN_HEIGHT+50 and jump_counter == 1 and (collide_left or collide_right) and PLAYER_GRAVITY!= 0 :     
    #         PLAYER_GRAVITY += -15
    #         collide_right = False
    #         collide_left = False
    #         # player_rect.x += 100
    #         jump_counter += 1
        


    if GAME_ACTIVE:
        # Background
        screen.blit(background_surf,(0,0))

        # Bottom Floor
        draw_floor(floor_surf,floor_rect,0,WIN_WIDTH)

        # Random Floors
        floor_sprite(floor_group)
        
        # Walls
        for i in range(len(wallList)):
            if i<3:
                place_surface(RWall_surf,wallList[i])
            else:
                place_surface(LWall_surf,wallList[i])

        # Player Movements and Logic
        PLAYER_GRAVITY += 0.7
        player_rect.y += (PLAYER_GRAVITY+offset_y)  
        if (player_rect.bottom >= WIN_HEIGHT-floor_surf.get_height()) and not PLAYER_THIRDWAY:
            player_rect.bottom = WIN_HEIGHT-floor_surf.get_height()
            PLAYER_GRAVITY = 0
            jump_counter = 0
        current_time = pygame.time.get_ticks()//1000
        # print(current_time)
        if current_time == 30 and not FLOOR_TIMER:
            FLOOR_TIMER += 1
            # current_time = 0
        # print(FLOOR_TIMER)
        # Collision mechanics 
        for floor in floor_group:
            if floor.rectsolid.colliderect(player_rect):
                if player_rect.bottom < floor.rectsolid.centery:
                    if PLAYER_GRAVITY > 0:
                        player_rect.bottom = floor.rectsolid.top
                        PLAYER_GRAVITY = 0
                        jump_counter = 0
        if player_rect.bottom < WIN_HEIGHT*(1/3):
            PLAYER_THIRDWAY = True
        if PLAYER_THIRDWAY and player_rect.top > 100:
            FLOOR_VELOCITY = 1
        elif (player_rect.top < scroll):
            player_rect.top = scroll
            offset_y = -PLAYER_GRAVITY
            FLOOR_VELOCITY = -(PLAYER_GRAVITY)

             
        # else:
        #     FLOOR_VELOCITY  = 2
        # print(pygame.sprite.Sprite.groups(Floor()))
        for floor in floor_group: 
            floor.rect. y += FLOOR_VELOCITY
            floor.rectsolid.y += FLOOR_VELOCITY
            # floor_yy += FLOOR_VELOCITY
            
            # if floor.rect.top > (WIN_HEIGHT + 100):
            #     floor_group.remove(floor)
            #     floor_group.add(Floor(randint(30,WIN_WIDTH-f_w-30), floor_yy, randint(120,400)))
            #     floor_yy -= 100
                
        

        # Player Rendering
        screen.blit(player_surf,player_rect)
        if player_rect.top > WIN_HEIGHT :
            screen.fill("Black")
            mixer.Channel(0).set_volume(0)
            # mixer.Channel(1).set_volume(1)
    

        # # random floor
        # if len(floor_rect_list)> 0:
        #     for i in range(len(floor_rect_list)):
        #         draw_floor(floor_rect_list[i][0],floor_rect_list[i][1], floor_rect_list[i][1]+450)
        

    
    pygame.display.update() 
    clock.tick(60) 