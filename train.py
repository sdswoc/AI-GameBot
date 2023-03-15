import random

import neat.nn
import pygame
from pygame import mixer
import os
from sys import exit
from random import randint
from classes import Floor, Wall, Player
from constants import *
import neat
import numpy as np
pygame.font.init()
pygame.init()



def reset(screen,floor_image):
    global floor_y, floor_yy, FLOOR_VELOCITY, floor_indices, floor_group, START_TIME, FALLING, GAME_ACTIVE
    START_TIME = pygame.time.get_ticks() // 1000
    FALLING = False
    floor_indices = list()
    floor_group = []
    floor_y = WIN_HEIGHT - 150
    floor_yy = WIN_HEIGHT - 150
    FLOOR_VELOCITY = 0

    bottom_floor = Floor(0, WIN_HEIGHT - 50, WIN_WIDTH)
    floor_group.append([0, bottom_floor])
    for i in range(MAX_FLOORS):
        f_w = randint(180, 370)
        f_x = randint(80, WIN_WIDTH - f_w - 80)


        floor = Floor(f_x, floor_yy, f_w)
        floor_group.append([i+1,floor])

        floor_yy -= 100
    # GAME_ACTIVE = menu["PlayGame"]


def draw_floor(floor_image, floor_group,screen):
    for floor_info in floor_group:
        floor = floor_info[1]
        floor.rect.x = floor.get_x()
        # floor.rect.y = floor.get_y()
        floor.rect.y += FLOOR_VELOCITY
        floor.rectsolid.y += FLOOR_VELOCITY
        while floor.rect.x < (floor.get_x() + floor.get_width()):
            screen.blit(floor.image, floor.rect)
            floor.rect.x += floor_image.get_width()




def handle_move(player, output, objects):
    decision = output
    indices = [i for i,x in enumerate(output) if x == max(output)]
    output_inx = random.choice(indices)
    for i in range(len(decision)):
        if i == output_inx:
            decision[i] = 1
        else:
            decision[i] = 0
    collide_right = False
    collide_left = False
    if (player.rect.left <= 51):
        collide_left = True
        player.rect.left = 51
    elif(player.rect.right >= WIN_WIDTH-51):
        collide_right = True
        player.rect.right = WIN_WIDTH - 51
    if decision[0] and not collide_left:
        player.move_left(PLAYER_VEL)
    elif decision[1] and not collide_right:
        player.move_right(PLAYER_VEL)
    elif decision[2] and player.on_floor:
        player.current_floor = player.rect.bottom
        player.jump()



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


def print_text(text, font, screen, pos, color=(202, 241, 222)):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)


def update_floor(floor, player):
    if floor[1].rect.bottom > WIN_HEIGHT + 200:
        # print("Me izz here")
        # removed_floor += 1
        floor_group.remove(floor)
        f_w = randint(180, 370)
        f_x = randint(80, WIN_WIDTH - f_w - 80)
        fr = Floor(f_x, floor_group[-1][1].rect.y - 100, f_w)
        floor_group.append([floor_group[-1][0]+1,fr])
        


def check_collision_and_score(floor, player,player_g):
    global FALLING, FLOOR_VELOCITY
    if floor[1].rectsolid.colliderect(player.rect):
        if player.rect.bottom < floor[1].rectsolid.centery:
            if player.y_vel > 0:
                player.landed()
                player.rect.bottom = floor[1].rectsolid.top
                player.y_vel = 0
                player.current_floor_index = floor[0]
                if player.current_floor_index > player.old_floor_index:
                    player.score_normal = 10*player.current_floor_index 
                    # player_g.fitness += 10

                    if player.bonus_y == 4:
                        player.score_bonus += 5
                        # player_g.fitness += 5
                    elif player.bonus_y == 8:
                        player.score_bonus += 15
                        # player_g.fitness += 15
                    player.old_floor_index = player.current_floor_index
                    player.score = player.score_normal + player.score_bonus
                if player.highest_floor_index < player.current_floor_index:
                    player.highest_floor_index = player.current_floor_index
        if (player.rect.top < 100) and not FALLING and FLOOR_VELOCITY == 0:
            FLOOR_VELOCITY += 1
            # FALLING = True
        if player.rect.right >= floor[1].rectsolid.right and player.x_vel != 0:
            # player_g.fitness += 0.4
            player.bonus_y = 4
            if abs(floor[1].rectsolid.centerx - floor_group[floor_group.index(floor) + 1][1].rectsolid.centerx) > 300:
                # player_g.fitness += 0.4
                player.bonus_y += 4
        elif player.rect.left <= floor[1].rectsolid.left and player.x_vel != 0:
            # player_g.fitness += 0.4
            player.bonus_y = 4
            if abs(floor[1].rectsolid.centerx - floor_group[floor_group.index(floor) + 1][1].rectsolid.centerx) > 200:
                # player_g.fitness += 0.4
                player.bonus_y += 4
        else:
            player.bonus_y = 0


def draw(floor_image,bg, floor_grp, wallgrp, players, screen,ge):
    global scroll, SCROLLING
    screen.blit(bg, (0, 0))
    draw_floor(floor_image, floor_group, screen)
    wallgrp.draw(screen)
    for player in players:
        for floor in floor_grp:
            floor[1].scroll(scroll)
            update_floor(floor, player)
            check_collision_and_score(floor, player, ge[players.index(player)])
        player.draw(screen)




def train_ai(genomes, config):
    global GAME_ACTIVE, START_TIME, FLOOR_VELOCITY, floor_yy, gen, floor_group, max_score,gen
    gen += 1

    # Defining pygame screen to draw assets and component
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Setting up caption (window title)
    pygame.display.set_caption("Icy Tower")

    # Loading and setting up window icon
    game_icon = pygame.image.load(os.path.join("icons", "icytowericon.png"))
    pygame.display.set_icon(game_icon)

    # Initialising pygame clock
    clock = pygame.time.Clock()

    # Loading background and floor image
    background_image = pygame.image.load(os.path.join("sprites", 'background.jpg')).convert()
    floor_image = pygame.image.load(os.path.join('sprites', 'icy2.png')).convert()

    # Getting floor rectangle
    floor_rect = floor_image.get_rect(topleft=(0, WIN_HEIGHT - floor_image.get_height()))
    # floor_group = []
    # Creating Bottom Floor
    bottom_floor = Floor(0, WIN_HEIGHT - 50, WIN_WIDTH)
    floor_group.append([0, bottom_floor])
    # Generating n (MAX_FLOORS) number of random floors
    for i in range(MAX_FLOORS):
        f_w = randint(180, 370)  # Generating Random width
        f_x = randint(80, WIN_WIDTH - f_w - 80)
  # Generating Random x position
        floor = Floor(f_x, floor_yy, f_w)  # Creating a Floor object with these values
        floor_group.append([i+1, floor])  # Adding all our floors to floor_group
        floor_yy -= 100  # Decrementing y location for next floor

    # Defining wallGroup (sprite group)
    wallGroup = pygame.sprite.Group()

    # Generating/Constructing Walls
    for i in range(3):
        wallR = Wall(804, i * 240, "right");
        wallL = Wall(45, i * 240, "left");
        wallGroup.add(wallR);
        wallGroup.add(wallL);

    # Loading Music/Sound Assets
    mixer.music.load(music_dict["gameBG"]);
    mixer.music.play(-1)  # Playing main game theme


    nets = [];
    ge = [];
    players = [];
    scores = [];
    highest_floors = [];
    # Setting Neural Network for each genome

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        player = Player(random.randint(80, WIN_WIDTH-80), WIN_HEIGHT - floor_image.get_height() - PLAYER_Y, PLAYER_X, PLAYER_Y)
        players.append(player)
        g.fitness = 0  # Setting initial fitness to 0
        ge.append(g)
        scores.append(player.score)
        highest_floors.append(player.highest_floor_index)

    GAME_ACTIVE = True

    # Getting time from pygame clock at the start of the game
    START_TIME = pygame.time.get_ticks() // 1000

    while True and len(players)>0:
        draw(floor_image, background_image, floor_group, wallGroup, players, screen, ge)
        player_height = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                # break

        if GAME_ACTIVE:
            current_time = pygame.time.get_ticks() // 1000 - START_TIME
            if current_time % 60 == 0 and current_time != 0 and FLOOR_VELOCITY < 4:
                FLOOR_VELOCITY += 1
                START_TIME += current_time
            for x, player in enumerate(players):
                if player.current_floor_index < player.highest_floor_index:
                    ge[x].fitness -= 5
                scores[x] = player.score
                highest_floors[x] = player.highest_floor_index
                ge[x].fitness = player.score
                player.loop(90)
                l = 0
                r = 0
                floor_data = []
                for i in range(len(floor_group)):
                    if floor_group[i][0] == player.current_floor_index :
                        for j in range(i,i+3):
                            # if (i+1) < len(floor_group):
                            if j == i :
                                l = player.rect.left - floor_group[j][1].rectsolid.right
                                r = player.rect.right - floor_group[j][1].rectsolid.left
                            else:
                                floor_data.append(floor_group[j][1].rectsolid.left)
                                floor_data.append(floor_group[j][1].rectsolid.y)
                                floor_data.append(floor_group[j][1].rectsolid.right)
                        break

                # max_score = max(scores)
                inputs = (FLOOR_VELOCITY,player.on_floor,player.rect.y, player.rect.x, player.x_vel, player.y_vel,  *floor_data, player.score,l,r)
                output = nets[x].activate(inputs)
                if ge[x].fitness < 0:
                    players.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                    scores.pop(x)
                    highest_floors.pop(x)

                handle_move(player,output, wallGroup)
                print_text(f"Score: {max(scores)}", TEXT_FONT, screen, (140, 10))
                print_text(f"Floors: {max(highest_floors)}", TEXT_FONT, screen, (240, 10))
                print_text(f"Gen: {gen}", TEXT_FONT, screen, (340, 10))

                if player.rect.top > WIN_HEIGHT:
                    ge[x].fitness -= 10
                    players.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    scores.pop(x)
                    highest_floors.pop(x)
        pygame.display.update()
        clock.tick(60)
    reset(screen, floor_image)
