import pygame, sys
from pygame.locals import *
import random
from constants import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, itemType, image, width, height, sound=None):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.imageWidth = self.image.get_width()
        self.imageHeight = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.itemType = itemType
        self.load_sound(sound)
        self.itemFall = random.randrange(-10,-2)

    def load_sound(self, sound):
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
        else:
            self.sound = None

    def play_sound(self):
        if self.sound != None:
            self.sound.play()

    def pick_up(self):
        self.play_sound()
        return self.itemType

    def gravity_check(self):
        if self.rect.y < DISPLAYHEIGHT - (self.imageHeight + 10):
            self.inAir = True
            self.itemFall += GRAVITY
            self.rect.y += self.itemFall
        else:
            self.inAir = False
            self.rect.y = DISPLAYHEIGHT - (self.imageHeight + 10)
            self.itemFall = 0

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_rect(self):
        return self.rect

    def get_bottom(self):
        return self.rect.bottom

    def get_top(self):
        return self.rect.top

    def get_left(self):
        return self.rect.left

    def get_right(self):
        return self.rect.right

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height
