import neat.nn
import pygame
from pygame import mixer
import os
from sys import exit
from random import randint
from classes import Floor, Wall, Player
from constants import *
import neat





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
    floor_group.append(bottom_floor)
    for i in range(MAX_FLOORS):
        f_w = randint(120, 400)
        f_x = randint(30, WIN_WIDTH - f_w - 30)

        floor = Floor(f_x, floor_yy, f_w)
        floor_group.append(floor)

        floor_yy -= 100
    # GAME_ACTIVE = menu["PlayGame"]


def draw_floor(floor_image, floor_group,screen):
    for floor in floor_group:
        floor.rect.x = floor.get_x()
        # floor.rect.y = floor.get_y()
        floor.rect.y += FLOOR_VELOCITY
        floor.rectsolid.y += FLOOR_VELOCITY
        while floor.rect.x < (floor.get_x() + floor.get_width()):
            screen.blit(floor.image, floor.rect)
            floor.rect.x += floor_image.get_width()


def welcome(screen,background_image):
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
        "PlayGame": True,
        "Instruction": False,
        "Profile": False,
        "HighScore": False,
        "LoadReplay": False,
        "Options": False,
        "Exit": False
    }
    clock = pygame.time.Clock()
    temp_im = pygame.image.load(os.path.join("sprites", "icyMan.png"))
    im = pygame.transform.rotozoom(temp_im, 0, 0.5)

    menu_img = pygame.image.load(os.path.join("sprites", "menu.png"))
    menu_img = pygame.transform.rotozoom(menu_img, 0, 1.3)
    menu_rect = menu_img.get_rect(center=(WIN_WIDTH // 2 + 150, WIN_HEIGHT // 2 + 150))

    hand_img = pygame.image.load(os.path.join("sprites", "hand.png"))
    hand_img = pygame.transform.rotozoom(hand_img, 0, 0.6)

    hand_rect = hand_img.get_rect(center=(WIN_WIDTH // 2 - 18, WIN_HEIGHT // 2 + 80))

    logo_im = pygame.image.load(os.path.join("sprites", "homescreen1.png")).convert_alpha()
    logo_im = pygame.transform.rotozoom(logo_im, 0, 1.2)
    logo_rect = logo_im.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 130))

    while active:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        SCREEN.blit(logo_im, logo_rect)
        rot_image = pygame.transform.rotate(im, tilt)
        new_rect = rot_image.get_rect(center=(WIN_WIDTH // 2 - 220, WIN_HEIGHT // 2 + 150))

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
            if (event.type == pygame.QUIT):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) or menu_dict["Exit"]:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_DOWN and index < (len(menu) - 1):
                    hand_rect.y += 28.5
                    menu_dict[menu[index]] = False
                    menu_dict[menu[index + 1]] = True
                    index += 1
                elif event.key == pygame.K_UP and index > 0:
                    hand_rect.y -= 28.5
                    menu_dict[menu[index]] = False
                    menu_dict[menu[index - 1]] = True
                    index -= 1
                elif event.key == pygame.K_RETURN:
                    return menu_dict
        pygame.display.update()
        clock.tick(60)


def handle_move(player, output, objects):
    decision = output.index(max(output))
    # print(decision)decision
    # keys = pygame.key.get_pressed()

    player.x_vel = 0  # If we don't do it player will continue to move untill we press some other key
    collide_left = collide(player, objects, -PLAYER_VEL)
    collide_right = collide(player, objects, PLAYER_VEL)
    # if keys[pygame.K_LEFT] and not collide_left:
    #     player.move_left(PLAYER_VEL)
    # if keys[pygame.K_RIGHT] and not collide_right:
    #     player.move_right(PLAYER_VEL)
    # # if event.type == pygame.KEYDOWN:
    # if ((keys[pygame.K_SPACE]) or (keys[pygame.K_UP])) and player.jump_count < 1:
    #     player.current_floor = player.rect.bottom
    #     player.jump()
    if decision == 0 and not collide_left:
        player.move_left(PLAYER_VEL)
    elif decision == 1 and not collide_right:
        player.move_right(PLAYER_VEL)
    else:
        player.current_floor = player.rect.bottom
        player.jump()

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


def print_text(text, font, screen, pos, color=(202, 241, 222)):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)


def update_floor(floor, player):
    if floor.rect.bottom > WIN_HEIGHT + 200:
        # print("Me izz here")
        # removed_floor += 1
        floor_group.remove(floor)
        f_w = randint(120, 400)
        f_x = randint(30, WIN_WIDTH - f_w - 30)
        floor = Floor(f_x, floor_group[-1].rect.y - 100, f_w)
        floor_group.append(floor)
        player.highest_floor_index -= 1
        player.current_floor_index -= 1
        player.old_floor_index -= 1


def check_collision_and_score(floor, player,player_g):
    global FALLING, FLOOR_VELOCITY
    if floor.rectsolid.colliderect(player.rect):
        if player.rect.bottom < floor.rectsolid.centery:
            if player.y_vel > 0:
                player.landed()
                player.rect.bottom = floor.rectsolid.top
                player.y_vel = 0
                player.current_floor_index = floor_group.index(floor)
                if player.current_floor_index > player.old_floor_index:
                    player.score += 10
                    player_g.fitness += 10

                    if player.bonus_y == 4:
                        player.score += 5
                        player_g.fitness += 5
                    elif player.bonus_y == 8:
                        player.score += 15
                        player_g.fitness += 15
                    player.old_floor_index = player.current_floor_index
                if player.highest_floor_index < player.current_floor_index:
                    player.highest_floor_index = player.current_floor_index
        if (player.rect.top < 100) and not FALLING and FLOOR_VELOCITY == 0:
            FLOOR_VELOCITY += 1
            FALLING = True
        if player.rect.right >= floor.rectsolid.right and player.x_vel != 0:
            player.bonus_y = 4
            if abs(floor.rectsolid.centerx - floor_group[floor_group.index(floor) + 1].rectsolid.centerx) > 300:
                player.bonus_y += 4
        elif player.rect.left <= floor.rectsolid.left and player.x_vel != 0:
            player.bonus_y = 4
            if abs(floor.rectsolid.centerx - floor_group[floor_group.index(floor) + 1].rectsolid.centerx) > 300:
                player.bonus_y += 4
        else:
            player.bonus_y = 0


def draw(floor_image,bg, floor_grp, wallgrp, players, screen,ge):
    global scroll
    screen.blit(bg, (0, 0))
    draw_floor(floor_image, floor_group, screen)
    wallgrp.draw(screen)
    # construct_floor(flr,floor_rect,0,WIN_WIDTH)
    for player in players:
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
            update_floor(floor, player)
            check_collision_and_score(floor, player, ge[players.index(player)])
        player.draw(screen)




def get_high_score():
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


def gameover(screen, score,menu,background_image):
    global GAME_ACTIVE
    gameover = pygame.image.load(os.path.join("sprites", "gameover.png"))
    gameover = pygame.transform.scale(gameover, (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(gameover, (0, 0))
    print_text(f"Score: {score}", TEXT_FONT, screen, (WIN_WIDTH // 2 - 100, 25))
    print_text(f"High Score: {get_high_score()}", TEXT_FONT, screen, (WIN_WIDTH // 2 + 100, 25))
    print_text("Press Space to Play Again", TEXT_FONT, screen, (WIN_WIDTH // 2, 450))
    print_text("Press Esc for Main Menu", TEXT_FONT, screen, (WIN_WIDTH // 2, 500))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (menu["Exit"]):
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = welcome(screen, background_image)
                GAME_ACTIVE = menu["PlayGame"]
            if event.key == pygame.K_SPACE:
                # tryagain.play()
                GAME_ACTIVE = True


gen = 1
def main(genomes, config):
    global GAME_ACTIVE, START_TIME, FLOOR_VELOCITY, floor_yy, gen
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

    # Creating Bottom Floor
    bottom_floor = Floor(0, WIN_HEIGHT - 50, WIN_WIDTH)
    floor_group.append(bottom_floor)

    # Generating n (MAX_FLOORS) number of random floors
    for i in range(MAX_FLOORS):
        f_w = randint(120, 400)  # Generating Random width
        f_x = randint(30, WIN_WIDTH - f_w - 30)  # Generating Random x position
        floor = Floor(f_x, floor_yy, f_w)  # Creating a Floor object with these values
        floor_group.append(floor)  # Adding all our floors to floor_group
        floor_yy -= 100  # Decrementing y location for next floor

    # Defining wallGroup (sprite group)
    wallGroup = pygame.sprite.Group()

    # Generating/Constructing Walls
    for i in range(3):
        wallR = Wall(804, i * 240, "right")
        wallL = Wall(45, i * 240, "left")
        wallGroup.add(wallR)
        wallGroup.add(wallL)

    # Loading Music/Sound Assets
    mixer.music.load(music_dict["gameBG"])
    gameOverSound = mixer.Sound(music_dict["gameOverSound"])
    tryagain = mixer.Sound(music_dict["tryagain"])
    mixer.music.play(-1)  # Playing main game theme

    # Creating player object
    # player = Player(WIN_WIDTH // 2, WIN_HEIGHT - floor_image.get_height() - PLAYER_Y, PLAYER_X, PLAYER_Y)

    nets = []
    ge = []
    players = []
    # Setting Neural Network for each genome

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Player(WIN_WIDTH // 2, WIN_HEIGHT - floor_image.get_height() - PLAYER_Y, PLAYER_X, PLAYER_Y))
        g.fitness = 0  # Setting initial fitness to 0
        ge.append(g)

    # Calling welcome (home screen) of game and getting the input of user back
    # menu = welcome(screen, background_image)

    # Setting GAME_ACTIVE as per user input
    GAME_ACTIVE = True

    # Getting time from pygame clock at the start of the game
    START_TIME = pygame.time.get_ticks() // 1000

    while True and len(players)>0:
        draw(floor_image, background_image, floor_group, wallGroup, players, screen, ge)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                break

        if GAME_ACTIVE:
            current_time = pygame.time.get_ticks() // 1000 - START_TIME
            if current_time % 30 == 0 and current_time != 0 and FLOOR_VELOCITY < 4:
                FLOOR_VELOCITY += 1
                START_TIME += current_time
            for x, player in enumerate(players):
                # ge[x].fitness += 0.1
                player.loop(180)

                # Giving input to the neural network and getting output
                inputs = (player.rect.y, player.rect.x, floor_group[player.current_floor_index + 1].rectsolid.top,floor_group[player.current_floor_index+1].rectsolid.left,floor_group[player.current_floor_index+1].rectsolid.right)
                output = nets[x].activate(inputs)
                # print(output)


                if ge[x].fitness < 0:
                    players.pop(x)
                    ge.pop(x)
                    nets.pop(x)

                handle_move(player,output, wallGroup)
                # print_text(f"Score: {player.score}", TEXT_FONT, screen, (140, 10))

                if player.rect.top > WIN_HEIGHT:
                    ge[x].fitness -= 10
                    players.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    # GAME_ACTIVE = False
                    # gameo.play()
                    # update_score(player.score)
            # if len(players) < 1 :
            #     GAME_ACTIVE = False
        # else:
        #     # gameover(screen, player.score, menu, background_image)
        #     reset(screen, floor_image)
        #     for _, g in genomes:
        #         net = neat.nn.FeedForwardNetwork.create(g, config)
        #         nets.append(net)
        #         players.append(
        #             Player(WIN_WIDTH // 2, WIN_HEIGHT - floor_image.get_height() - PLAYER_Y, PLAYER_X, PLAYER_Y))
        #         g.fitness = 0  # Setting initial fitness to 0
        #         ge.append(g)
        #     GAME_ACTIVE = True
                # mixer.Channel(0).set_volume(1)

        pygame.display.update()
        clock.tick(180)
    reset(screen, floor_image)
