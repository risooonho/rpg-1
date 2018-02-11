import pygame, sys
from pygame.locals import *
import random
from ItemsClasses import *
from PlayerClasses import *
from constants import *

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

DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("RPG")

#Text
inventoryFont = pygame.font.SysFont('georgia', 32)
selectFont = pygame.font.SysFont('georgia', 32)
selectFont.set_underline(True)

#Images
charImgs = ('characters/guy0.png', 'characters/guy1.png', 'characters/guy2.png', 'characters/guy3.png')
coinImg = 'items/coin0.png'
swordImg = 'items/sword.png'
background = pygame.image.load("backgrounds/forest.jpg").convert()
background = pygame.transform.scale(background,(DISPLAYWIDTH, DISPLAYHEIGHT))

#Backgrounds
backgroundNumber = 0

backgrounds = []
backgrounds.append(pygame.image.load("backgrounds/forest.jpg").convert())
backgrounds[-1] = pygame.transform.scale(backgrounds[-1],(DISPLAYWIDTH, DISPLAYHEIGHT))
backgrounds.append(pygame.image.load("backgrounds/desert.jpg").convert())
backgrounds[-1] = pygame.transform.scale(backgrounds[-1],(DISPLAYWIDTH, DISPLAYHEIGHT))

#Sounds
coinSound = 'sounds/coin.wav'
swordSound = 'sounds/sword.wav'

#Creates sprite group of items
items = pygame.sprite.Group()
#Creates multiple coins
coinList = []
for i in range(0,30):
    coinList.append(Item(random.randrange(0,DISPLAYWIDTH), 500, {'coin':1}, coinImg, 16, 16, coinSound))
#Creates sword
sword = Item(700,500, {'sword':1}, swordImg, 36, 36, swordSound)
#Adds items to sprite group
items.add(coinList, sword)

#Creates sprite group for walls
walls = pygame.sprite.Group()
#Creates walls
floor = Wall(0, DISPLAYHEIGHT, DISPLAYWIDTH, 10)
wall1 = Wall(300, DISPLAYHEIGHT-100, 300, 30)
wall2 = Wall(300, DISPLAYHEIGHT-400, 30, 300)
#Adds walls to wall group
walls.add(floor, wall1, wall2)

#Starting coords
player = Player(DISPLAYWIDTH/2, 50, charImgs)

def level():
    moveX, moveY = 0, 0
    global backgroundNumber
    #Game Loop
    while True:
        # print(player.jumping, moveY)

        #Gravity
        if player.jumping == True:
            moveY += GRAVITY
        else:
            moveY = 0

        #Quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
                # if event.key == pygame.K_DOWN:
                #     moveY += 10
                if event.key == pygame.K_e:
                    moveX = 0
                    moveY = 0
                    inventoryMenu()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moveX += 5
                if event.key == pygame.K_RIGHT:
                    moveX += -5

            #More events

        #Background change
        if player.rect.x > DISPLAYWIDTH and (len(backgrounds) - 1) > backgroundNumber:
            backgroundNumber += 1
            player.rect.x = 0
        elif player.rect.x < 0 and backgroundNumber > 0:
            backgroundNumber -= 1
            player.rect.x = DISPLAYWIDTH

        DISPLAYSURF.blit(backgrounds[backgroundNumber], (0,0))
        #Update and draw player
        player.update(moveX, moveY, items, walls)
        player.draw(DISPLAYSURF)
        player.totalx = (DISPLAYWIDTH * backgroundNumber) + player.rect.x
        player.totaly = player.rect.y
        #Update and draw items
        itemList = items.sprites()
        for i in range(0,len(itemList)):
            itemList[i].gravity_check()
        items.draw(DISPLAYSURF)
        #On-screen messages
        if len(player.collisionList) > 0:
            if list(player.collisionList[0].itemType.keys())[0] != "coin":
                popuptext = inventoryFont.render('You picked up a ' + list(player.collisionList[0].itemType.keys())[0], True, GREEN)
            else:
                popuptext = inventoryFont.render('Coins: ' + str(player.inventory.get('coin')), True, GREEN)
        if player.pickUpCoolDown > 0:
            DISPLAYSURF.blit(popuptext, (0, 0))
            player.pickUpCoolDown -= 1

        #Draw walls
        walls.draw(DISPLAYSURF)

        FPSCLOCK.tick(FPS)
        pygame.display.update()

scroll = pygame.image.load("backgrounds/scroll.png").convert_alpha()
scroll = pygame.transform.scale(scroll, (844, 543))
#Defaults
scrollX = 90
scrollY = 70

def inventoryMenu():
    playerInv = player.get_inventory()
    invKeys = []
    if playerInv == {}:
        emptyInvMessage()
    else:
        for key in playerInv.keys():
            invKeys.append(key)
        if len(invKeys) <= 8:
            smallInvMenu(playerInv, invKeys)

def emptyInvMessage():
    HeaderText = inventoryFont.render('--Inventory--', True, BLACK)
    EmptyText = inventoryFont.render('Inventory is empty', True, BLACK)
    xcoord = 212
    ycoord = 150
    Open = True
    while Open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    Open = False
        DISPLAYSURF.blit(scroll, (scrollX, scrollY))
        DISPLAYSURF.blit(HeaderText, (xcoord, ycoord))
        DISPLAYSURF.blit(EmptyText, (xcoord, ycoord+50))
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def smallInvMenu(playerInv, invKeys):
    HeaderText = inventoryFont.render('--Inventory--', True, BLACK)
    xcoord = 212
    Open = True
    selectNum = 0
    while Open:
        ycoord = 150
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    Open = False
                if event.key == pygame.K_UP:
                    if selectNum > 0:
                        selectNum -= 1
                    else:
                        selectNum = len(invKeys) - 1
                if event.key == pygame.K_DOWN:
                    if selectNum < len(invKeys) - 1:
                        selectNum += 1
                    else:
                        selectNum = 0
        DISPLAYSURF.blit(scroll, (scrollX, scrollY))
        DISPLAYSURF.blit(HeaderText, (xcoord, ycoord))
        ycoord += 50
        for key in invKeys:
            if invKeys[selectNum] == key:
                itemtext = selectFont.render(key + '---' + str(playerInv[key]), True, BLACK)
            else:
                itemtext = inventoryFont.render(key + '---' + str(playerInv[key]), True, BLACK)
            DISPLAYSURF.blit(itemtext, (xcoord, ycoord))
            ycoord += 40
        FPSCLOCK.tick(FPS)
        pygame.display.update()

level()
