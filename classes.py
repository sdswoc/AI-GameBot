import pygame
import os

class Player(pygame.sprite.Sprite):
    # we can use sprites collide method
    COLOR = (255, 0, 0)
    GRAVITY = 1  # Setting default gravity

    def __init__(self, x, y, PLAYER_X, PLAYER_Y):
        super().__init__()
        self.image = pygame.image.load('sprites/icyMan.png')
        self.image = pygame.transform.scale(self.image, (PLAYER_X, PLAYER_Y))
        self.rect = pygame.Rect(x, y, PLAYER_X, PLAYER_Y)
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
        self.jump_count += 1
        self.on_floor = False

        self.current_height = self.rect.y
        if self.jump_count == 1:
            self.y_vel = -self.GRAVITY * 15 - self.bonus_y

            self.count = 0
        # elif self.jump_count == 2 :

    def move(self, dx, dy):
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

    def loop(self, fps):
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
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window, offset_x=0):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def get_score(self):
        return self.score

    def update_score(self):
        self.score += 10


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        self.width = width
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('sprites','icy2.png')).convert()
        self.imagesolid = pygame.transform.scale(self.image, (self.width, self.image.get_height()))

        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rectsolid = self.imagesolid.get_rect(topleft=(self.x, self.y))

    def get_width(self):
        return self.width

    def get_x(self): return self.x

    def get_y(self): return self.y

    def scroll(self, scroll):
        self.rect.y += scroll
        self.rectsolid.y += scroll


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, dire):
        super().__init__()
        self.x = x
        self.y = y
        self.dire = dire
        self.image = pygame.transform.rotozoom(pygame.image.load('sprites/wall2.png').convert_alpha(), 0, 0.4)
        self.rect = self.image.get_rect(topright=(self.x, self.y))
        if self.dire == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
