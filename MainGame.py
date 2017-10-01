import pygame, sys
from pygame.locals import *

#Colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)

pygame.init()
DISPLAYWIDTH = 1024
DISPLAYHEIGHT = 683
PLAYERSCALEW = 80
PLAYERSCALEY = 120
DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
FPS = 60
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("RPG")

#Player class------------------------------:
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        pygame.sprite.Sprite.__init__(self)
        self.loadImages(images)
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

    def loadImages(self, images):
        self.charWidth = PLAYERSCALEW
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
        self.moveSprite(movex, movey)
        self.itemsCollision(items)
        self.render()

    def draw(self, Surface):
        Surface.blit(self.image, (self.rect.x, self.rect.y))

    def moveSprite(self, movex, movey):
        oldX = self.rect.x
        oldY = self.rect.y
        self.rect.x += movex
        self.rect.y += movey
        self.movementCheck(oldX, oldY)

    def movementCheck(self, oldx, oldy):
        #Jumping check/ Floor check
        if self.rect.y < (DISPLAYHEIGHT - self.charHeight):
            self.jumping = True
        else:
            self.jumping = False
            self.rect.y = (DISPLAYHEIGHT - self.charHeight)
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
        self.chooseImageNum()
        if self.left == True:
            self.image = pygame.transform.flip(self.images[self.imageNum], True, False)
        else:
            self.image = self.images[self.imageNum]

    def chooseImageNum(self):
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

    def itemsCollision(self, items):
        collisionList = pygame.sprite.spritecollide(self, items, True)
        for collision in collisionList:
            item = collision.pickUp()
            #self.updateInventory(item)

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, itemType, image, sound=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.itemType = itemType
        self.loadSound(sound)

    def loadSound(self, sound):
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
        else:
            self.sound = None

    def playSound(self):
        if self.sound != None:
            self.sound.play()

    def pickUp(self):
        self.playSound()
        return self.itemType


#Images
charImgs = ('characters/guy0.png', 'characters/guy1.png', 'characters/guy2.png', 'characters/guy3.png')
coinImg = 'items/coin0.png'
background = pygame.image.load("backgrounds/forest.jpg").convert()
background = pygame.transform.scale(background,(DISPLAYWIDTH, DISPLAYHEIGHT))

#Sounds
coinSound = 'sounds/coin.wav'

items = pygame.sprite.Group() #Creates sprite group
coin = Item(500, 355, {'coin':1}, coinImg, coinSound) #Creates coin item
coin2 = Item(600, 500, {'coin':1}, coinImg, coinSound) #Creates coin item
items.add(coin, coin2) #Adds coin to sprite group

#Starting coords
player = Player(DISPLAYWIDTH/2, DISPLAYHEIGHT - PLAYERSCALEY, charImgs)

def level():
    moveX, moveY = 0, 0
    while True:#Game Loop
        #Gravity
        if player.jumping == True:
            moveY += 0.5
        else:
            moveY = 0

        #Quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Player movement (side view)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveX += -5
                if event.key == pygame.K_RIGHT:
                    moveX += 5
                if event.key == pygame.K_UP and player.jumping == False:
                    moveY += -10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moveX += 5
                if event.key == pygame.K_RIGHT:
                    moveX += -5


            #Player movement (top view)
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_a:
            #         moveX = -5
            #     if event.key == pygame.K_d:
            #         moveX = 5
            #     if event.key == pygame.K_w:
            #         moveY = -5
            #     if event.key == pygame.K_s:
            #         moveY = 5
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_a:
            #         moveX = 0
            #     if event.key == pygame.K_d:
            #         moveX = 0
            #     if event.key == pygame.K_w:
            #         moveY = 0
            #     if event.key == pygame.K_s:
            #         moveY = 0

            #More events


        DISPLAYSURF.blit(background, (0,0))
        player.update(moveX, moveY, items)
        player.draw(DISPLAYSURF)
        items.draw(DISPLAYSURF)
        FPSCLOCK.tick(FPS)
        pygame.display.update()

level()
