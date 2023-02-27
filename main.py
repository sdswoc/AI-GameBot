import pygame
import sys
from sys import exit 
from pygame import mixer
from random import randint
import os


pygame.init()
mixer.init()

global PLAYER_THIRDWAY, floor_y, floor_yy, floor_group, bottom_floor
TEXT_FONT = pygame.font.Font('fonts/agency_fb.ttf', 25)
# HOME_X = 400
# HOME_Y = 300
PLAYER_VEL = 5
OFFSET_Y = 50
scroll = 0
PLAYER_X = 208/6.5
PLAYER_Y = 411/6.5
WIN_WIDTH = 800  
WIN_HEIGHT = 600
GAME_ACTIVE = True
MAX_FLOORS = 50
PLAYER_THIRDWAY= False
PLAYER_2THIRDWAY = False
FLOOR_VELOCITY = 0

floor_indices = []
START_TIME = 0
floor_y = WIN_HEIGHT-150
floor_yy = WIN_HEIGHT -150
floor_group = list()
removed_floor = 0
music_dict =  {
    "gameBG" : os.path.join("music","gameBG.mp3"),
    "theme" : os.path.join("music","theme.mp3"),
    "gameover" : os.path.join("music","gameover.ogg"),
    "menuchoose" : os.path.join("music","menuchoose.ogg"),
    "menuchange" : os.path.join("music","menuchange.ogg"),
    "tryagain" : os.path.join("music","tryagain.ogg"),
    "hurryup" : os.path.join("music","hurryup.ogg"),
}



def reset():
    global floor_y,floor_yy, FLOOR_VELOCITY, floor_indices, floor_group, START_TIME, PLAYER_THIRDWAY, GAME_ACTIVE
    START_TIME = pygame.time.get_ticks()//1000
    player.score = 0
    PLAYER_THIRDWAY = False
    player.current_floor = WIN_HEIGHT - floor_surf.get_height() - PLAYER_Y
    floor_indices = list()
    floor_group = []
    floor_y = WIN_HEIGHT-150
    floor_yy = WIN_HEIGHT -150
    FLOOR_VELOCITY = 0
    player.rect.x = WIN_WIDTH//2
    player.rect.y = WIN_HEIGHT - floor_surf.get_height() - PLAYER_Y
    player.y_vel = 0
    player.jump_count = 0
    player.current_floor_index = 0
    player.highest_floor_index = 0
    player.old_floor_index = 0

    bottom_floor = Floor(0,WIN_HEIGHT-50,WIN_WIDTH)
    floor_group.append(bottom_floor)
    for i in range(MAX_FLOORS):
        f_w = randint(120,400)
        f_x = randint(30,WIN_WIDTH-f_w-30) 
    
        floor = Floor(f_x, floor_yy, f_w)
        floor_group.append(floor)

        floor_yy -= 100
    GAME_ACTIVE = menu["PlayGame"]

class Player(pygame.sprite.Sprite):
    # we can use sprites collide method
    COLOR = (255,0,0)
    GRAVITY = 1 # Setting default gravity
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('sprites/icyMan.png')
        self.image = pygame.transform.scale(self.image, (PLAYER_X, PLAYER_Y))
        self.rect = pygame.Rect(x,y,PLAYER_X,PLAYER_Y)
        self.x_vel = 0  
        self.y_vel = 0
        self.mask = None
        self.fall_count = 0
        self.jump_count = 0
        self.score = 0
        self.current_floor = 0
        self.highest_floor = 0
        self.old_floor = 0
        self.current_floor_index = 0
        self.old_floor_index = 0
        self.highest_floor_index = 0
        self.on_floor = True
        self.collision = True
        # self.jump = False
        self.combo = False
        self.comboadded = True
        self.bonus_y = 0 
        self.current_height = self.rect.y
        self.current_y = self.rect.y

    def jump(self):
        self.jump_count+=1
        self.on_floor = False
        
        self.current_height = self.rect.y
        if self.jump_count == 1:
            self.y_vel = -self.GRAVITY * 15 - self.bonus_y
            
            self.count = 0
        # elif self.jump_count == 2 : 



    def move(self,dx,dy):
        """
        Function will move the player
        dx = change in x
        dy = change in y
        """
        self.rect.x += dx
        self.rect.y += dy 
        
    def move_left(self, vel):
        self.x_vel = -vel
    def move_right(self, vel):
        self.x_vel = vel
    def loop(self,fps):
        """loop to move player and control animation """
        # Trying to get more realistic gravity
        # self.y_vel += min(1,(self.fall_count/fps)*self.GRAVITY)
        self.y_vel += self.GRAVITY
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1 
        # self.update_sprite()
        self.update()
    
    def landed(self):
        self.on_floor = True
        self.jump_count = 0
        self.fall_count = 0
        self.y_vel = 0
        self.old_floor = self.current_floor
        # self.score += 10

    def update(self):
        self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self,window, offset_x=0):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))
    def get_score(self):
        return self.score
    def update_score(self):
        self.score+=10


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
    def scroll(self, scroll):
        self.rect.y += scroll
        self.rectsolid.y += scroll


class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,dire):
        super().__init__()
        self.x = x
        self.y = y
        self.dire = dire
        self.image = pygame.transform.rotozoom(pygame.image.load('sprites/wall2.png').convert_alpha(),0,0.4)
        self.rect = self.image.get_rect(topright = (self.x, self.y))
        if self.dire == "left" :
            self.image = pygame.transform.flip(self.image, True, False)
        
    def draw(self,screen):
        screen.blit(self.image,self.rect)



def place_surface (surf,rect):
    screen.blit(surf,rect)



# def construct_floor(floor,rect,st,en):
#     rect.x = st
#     while rect.x<en:
#         if PLAYER_THIRDWAY:
#             rect.top += FLOOR_VELOCITY
#         screen.blit(floor, rect)
#         rect.x += floor.get_width()
def draw_floor(floor_group):
    for floor in floor_group:
        floor.rect.x = floor.get_x()
        # floor.rect.y = floor.get_y() 
        floor.rect.y += FLOOR_VELOCITY
        floor.rectsolid.y += FLOOR_VELOCITY
        while floor.rect.x < (floor.get_x() + floor.get_width()):
            screen.blit(floor.image, floor.rect)
            floor.rect.x += floor_surf.get_width()


def welcome(screen):
    
    
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
        
def handle_move(player,objects):
    keys = pygame.key.get_pressed()


    player.x_vel = 0 # If we don't do it player will continue to move untill we press some other key
    collide_left = collide(player, objects, -PLAYER_VEL)
    collide_right = collide(player, objects, PLAYER_VEL)
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    
    # handle_vertical_collition(player, objects, player.y_vel)


# Handling horizontal collision
def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided_object
def print_text(text,font,screen,pos, color = (202, 241, 222)):
    text_surface = font.render(text,True, color)
    text_rect = text_surface.get_rect(center = pos)
    screen.blit(text_surface,text_rect)

def draw(bg, floor_grp,wallgrp,player):
    global FLOOR_VELOCITY
    global PLAYER_THIRDWAY 
    global removed_floor
    global scroll

    # construct_floor(flr,floor_rect,0,WIN_WIDTH)
    if player.rect.top <= OFFSET_Y:
            if player.y_vel < 0:
                # player.y_vel = 0
                player.rect.top = OFFSET_Y
                scroll = -player.y_vel
                # player.move(0,scroll)
            else: 
                scroll = 0
    for floor in floor_grp:
        # print(floor_indices)
        floor.scroll(scroll)
        if floor.rect.bottom > WIN_HEIGHT + 200:
            # print("Me izz here")
            # removed_floor += 1
            floor_group.remove(floor)
            f_w = randint(120,400)
            f_x = randint(30,WIN_WIDTH-f_w-30) 
            floor = Floor(f_x, floor_group[-1].rect.y - 100, f_w)
            floor_group.append(floor)
            player.highest_floor_index -= 1
            player.current_floor_index -= 1
            player.old_floor_index -= 1
                
        if floor.rectsolid.colliderect(player.rect):
            if player.rect.bottom < floor.rectsolid.centery:
                if player.y_vel> 0:
                    player.landed()
                    player.rect.bottom = floor.rectsolid.top
                    player.y_vel = 0
                    player.current_floor_index = floor_group.index(floor)
                    if player.current_floor_index > player.old_floor_index :
                        player.score += 10
                        if player.bonus_y == 4:
                            player.score+=5
                        elif player.bonus_y == 8:
                            player.score += 15
                        player.old_floor_index = player.current_floor_index
                    if player.highest_floor_index < player.current_floor_index :
                        player.highest_floor_index = player.current_floor_index
            if (player.rect.top < 100) and not PLAYER_THIRDWAY and FLOOR_VELOCITY==0 :
                FLOOR_VELOCITY += 1
                PLAYER_THIRDWAY= True
            if player.rect.right >= floor.rectsolid.right and player.x_vel!= 0 :
                player.bonus_y = 4
                if abs(floor.rectsolid.centerx - floor_group[floor_group.index(floor)+1].rectsolid.centerx) > 300:
                    player.bonus_y += 4
            elif player.rect.left <= floor.rectsolid.left and player.x_vel != 0 :
                player.bonus_y = 4
                if abs(floor.rectsolid.centerx - floor_group[floor_group.index(floor)+1].rectsolid.centerx) > 300:
                    player.bonus_y += 4
            else:
                player.bonus_y = 0
    
    
                
    
    screen.blit(bg, (0,0))
    draw_floor(floor_group)
    for wall in wallgrp:
        wall.draw(screen)
    player.draw(screen)

def get_high_score() :
    fr = open("db/score.txt", "r")
    highscore = fr.readline()
    return int(highscore)

def update_score(score):
    f = open("db/score.txt", "r")
    old = f.readline()
    f.close()
    if score > int(old):
        fw = open("db/score.txt", "w")
        fw.write(str(score))

def gameover():
    global GAME_ACTIVE,menu
    gameover = pygame.image.load(os.path.join("sprites","gameover.png"))
    gameover = pygame.transform.scale(gameover,(WIN_WIDTH,WIN_HEIGHT))
    screen.blit(gameover,(0,0))
    print_text(f"Score: {player.score}",TEXT_FONT,screen,(WIN_WIDTH//2 - 100,25))
    print_text(f"High Score: {get_high_score()}",TEXT_FONT,screen,(WIN_WIDTH//2 + 100,25))
    print_text("Press Space to Play Again",TEXT_FONT,screen,(WIN_WIDTH//2,450))
    print_text("Press Esc for Main Menu",TEXT_FONT,screen,(WIN_WIDTH//2,500))
    for event in pygame.event.get()  :
            if event.type == pygame.QUIT or (menu["Exit"]):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = welcome(screen)
                    GAME_ACTIVE = menu["PlayGame"] 
                if event.key == pygame.K_SPACE:
                    tryagain.play()
                    GAME_ACTIVE = True


screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) 
# screen.fill('White')



pygame.display.set_caption("Icy Tower")



game_icon = pygame.image.load(os.path.join("icons","icytowericon.png"))
pygame.display.set_icon(game_icon)



clock = pygame.time.Clock()



background_surf = pygame.image.load(os.path.join("sprites",'background.jpg')).convert()




wallGroup = pygame.sprite.Group()
for i in range(3):
    wallR = Wall(804,i*240,"right")
    wallL = Wall(45,i*240,"left")
    wallGroup.add(wallR)
    wallGroup.add(wallL)




floor_surf = pygame.image.load(os.path.join('sprites','icy2.png')).convert()                 
floor_rect = floor_surf.get_rect(topleft = (0,WIN_HEIGHT-floor_surf.get_height()))




bottom_floor = Floor(0,WIN_HEIGHT-50,WIN_WIDTH)
floor_group.append(bottom_floor)
for i in range(MAX_FLOORS):
    f_w = randint(120,400)
    f_x = randint(30,WIN_WIDTH-f_w-30) 
    
    floor = Floor(f_x, floor_yy, f_w)
    
    floor_group.append(floor)
    floor_yy -= 100

floor_rect_list = []

gameBG = mixer.music.load(music_dict["gameBG"]) 
gameo = mixer.Sound(music_dict["gameover"])
tryagain = mixer.Sound(music_dict["tryagain"])
mixer.music.play(-1)
mixer.music.set_volume(1)



player = Player(WIN_WIDTH//2,WIN_HEIGHT - floor_surf.get_height() - PLAYER_Y )


menu = welcome(screen)
GAME_ACTIVE = menu["PlayGame"]
START_TIME = pygame.time.get_ticks()//1000


while True :
    # collide_left = False
    # collide_right = False
    for event in pygame.event.get()  :
        if event.type == pygame.QUIT or (menu["Exit"]):
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if ((event.key == pygame.K_SPACE)or (event.key == pygame.K_UP)) and player.jump_count < 1:
                player.current_floor = player.rect.bottom
                player.jump()
            
            
                
    if GAME_ACTIVE:    
        draw(background_surf,floor_group,wallGroup,player)
        current_time = pygame.time.get_ticks()//1000 - START_TIME
        if current_time % 30 == 0 and current_time!=0 and FLOOR_VELOCITY<4:
            FLOOR_VELOCITY += 1
            START_TIME += current_time
        player.loop(60)
        handle_move(player,wallGroup)
        print_text(f"Score: {player.score}",TEXT_FONT,screen,(140,10))

        if player.rect.top > WIN_HEIGHT :
            # screen.fill("Black")
            GAME_ACTIVE = False
            gameo.play()
            update_score(player.score)
    else:
        gameover()
        


        
        if GAME_ACTIVE:
            reset()
            # player.rect.bottom = WIN_HEIGHT - floor_surf.get_height() - PLAYER_Y
            # player.rect.centerx = WIN_WIDTH//2
            
            
            # for floor in floor_group:
            #     floor.rectsolid.bottom = floor_y
            #     floor_y -= 100
            mixer.Channel(0).set_volume(0.05)
            

    pygame.display.update() 
    clock.tick(60) 