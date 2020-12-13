from pygame import *
import pygame
import time
import random

#True while game is being played.
running = True

#STATIC GLOBALS
#Color defs
BLACK = (0,0,0)
WHITE = (255, 255, 255)
FOOD = (0, 255, 0)
SNAKE = (0, 0, 255)

#Window size defs
WINHEIGHT = 300
WINWIDTH = 300

#Object size defs
BLOCKSIZE = 10

#Screen size
SCREEN = pygame.display.set_mode((WINHEIGHT, WINWIDTH))

#DYNAMIC GLOBALS
#Snake Coordinates
COORDS = [[10, 10]]
#Snake count
COUNT = 1
#Snake head 
HEADX = 10
HEADY = 10

class Game():
    def __init__(self):
        self.player = Player()
        self.food = Food()

    #on game start
    def onInit(self):
        pygame.init()
        self.drawGrid()
        pygame.display.flip()

    #draws game grid
    def drawGrid(self):
        SCREEN.fill(WHITE)
        for x in range(WINWIDTH // BLOCKSIZE):
            for y in range(WINWIDTH // BLOCKSIZE):
                rect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE,
                                   BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(SCREEN, BLACK, rect, 1)

    #On game rander
    def onRender(self):
        pygame.display.flip()

    #while game is running
    def onRun(self): 
        global HEADX
        global HEADY
        global COUNT

        xDirection = 0
        yDirection = 0
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_UP and yDirection != BLOCKSIZE:
                        yDirection = -BLOCKSIZE
                        xDirection = 0

                    elif event.key == pygame.K_DOWN and yDirection != -BLOCKSIZE:
                        yDirection = BLOCKSIZE
                        xDirection = 0
                        directionLockout = 0

                    elif event.key == pygame.K_LEFT and xDirection != BLOCKSIZE:
                        yDirection = 0
                        xDirection = -BLOCKSIZE

                    elif event.key == pygame.K_RIGHT and xDirection != -BLOCKSIZE:
                        yDirection = 0
                        xDirection = BLOCKSIZE

                    elif event.key == pygame.K_e:
                        COUNT += 1
            
            HEADX += xDirection
            HEADY += yDirection

            self.drawGrid()
            self.player.snakePeriodic()
            self.food.foodPeriodic()
            self.onRender

            pygame.display.update()
            time.sleep(75.0 / 1000.0)

class Player: #The player
    def snakePeriodic(self): #Snake's periodic, governs how the snake acts every tick.
        global COORDS
        global HEADX
        global HEADY

        snakeHead = [] #Snake  head location
        snakeHead.extend((HEADX, HEADY))

        COORDS.append(snakeHead)

        if len(COORDS) > COUNT: #Ensures snake follows the count
            del COORDS[0]
        if snakeHead in COORDS[:-1] or HEADX >= WINHEIGHT or HEADX < 0 or HEADY >= WINWIDTH or HEADY < 0: #Kill conditions
            pygame.quit()
        
        for HEADX, HEADY in COORDS: #Draws snake
            pygame.draw.rect(
                SCREEN, SNAKE, [HEADX, HEADY, BLOCKSIZE, BLOCKSIZE])

class Food: #food's periodic, governs how food acts every tick. 
    def __init__(self):
        self.x = random.randrange(BLOCKSIZE, WINWIDTH, BLOCKSIZE)
        self.y = random.randrange(BLOCKSIZE, WINHEIGHT, BLOCKSIZE)
    

    def foodPeriodic(self):
        global COUNT
        if self.x == HEADX and self.y == HEADY: #Eating conditional
            COUNT += 1
            self.x = random.randrange(BLOCKSIZE, WINWIDTH, BLOCKSIZE)
            self.y = random.randrange(BLOCKSIZE, WINWIDTH, BLOCKSIZE)

        pygame.draw.rect(SCREEN, FOOD,[self.x, self.y, BLOCKSIZE, BLOCKSIZE])
                

        
        
if __name__ == "__main__":
    App = Game()
    App.onInit()
    App.onRun()
