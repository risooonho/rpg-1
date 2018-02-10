import pygame, sys
from pygame.locals import *
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        pygame.sprite.Sprite.__init__(self)
        self.load_images(images)
        self.image = self.i0
        self.imageNum = 0
        self.timeTarget = 10
        self.timeNum = 0
        self.rect = self.image.get_rect()
        self.rect.x = x #Left
        self.rect.y = y #Top
        self.left = False
        self.moving = False
        self.jumping = False
        self.inventory = {}
        self.pickUpCoolDown = 0

    def load_images(self, images):
        self.charWidth = PLAYERSCALEX
        self.charHeight = PLAYERSCALEY
        self.i0 = pygame.image.load(images[0]).convert_alpha()
        self.i0 = pygame.transform.scale(self.i0, (self.charWidth, self.charHeight))
        self.i1 = pygame.image.load(images[1]).convert_alpha()
        self.i1 = pygame.transform.scale(self.i1, (self.charWidth, self.charHeight))
        self.i2 = pygame.image.load(images[2]).convert_alpha()
        self.i2 = pygame.transform.scale(self.i2, (self.charWidth, self.charHeight))
        self.i3 = pygame.image.load(images[3]).convert_alpha()
        self.i3 = pygame.transform.scale(self.i3, (self.charWidth, self.charHeight))
        self.images = (self.i0, self.i1, self.i2, self.i3)

    def update(self, movex, movey, items):
        self.move_sprite(movex, movey)
        self.items_coll(items)
        self.render()

    def draw(self, Surface):
        Surface.blit(self.image, (self.rect.x, self.rect.y))

    def move_sprite(self, movex, movey):
        oldX = self.rect.x
        oldY = self.rect.y
        self.rect.x += movex
        self.rect.y += movey
        self.movement_check(oldX, oldY)

    def movement_check(self, oldx, oldy):
        #Jumping check/ Floor check
        if self.rect.y < (DISPLAYHEIGHT - (self.charHeight + 10)):
            self.jumping = True
        else:
            self.jumping = False
            self.rect.y = (DISPLAYHEIGHT - (self.charHeight + 10))
        #Move check
        if self.rect.x == oldx and self.rect.y == oldy and self.jumping == False:
            self.moving = False
        else:
            self.moving = True
            if self.rect.x > oldx:
                self.left = False
            elif self.rect.x < oldx:
                self.left = True

    def render(self):
        self.choose_imageNum()
        if self.left == True:
            self.image = pygame.transform.flip(self.images[self.imageNum], True, False)
        else:
            self.image = self.images[self.imageNum]

    def choose_imageNum(self):
        if self.moving == True and self.jumping == False:
            self.timeNum += 1
            if self.timeNum >= self.timeTarget:
                if self.imageNum < 3:
                    self.imageNum += 1
                else:
                    self.imageNum = 0
                self.timeNum = 0
        else:
            self.imageNum = 0

    def items_coll(self, items):
        self.collisionList = pygame.sprite.spritecollide(self, items, True)
        for collision in self.collisionList:
            item = collision.pick_up()
            self.update_inventory(item)
            print(self.inventory)
            self.pickUpCoolDown = 50

    def update_inventory(self, item):
        for key in item.keys():
            if key in self.inventory:
                self.inventory[key] += item[key]
            else:
                self.inventory = dict(list(self.inventory.items()) + list(item.items()))

    def get_inventory(self):
        return self.inventory
