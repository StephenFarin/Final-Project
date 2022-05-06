import random, pygame, sys
from pygame.math import Vector2
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
CELLSIZE = 8
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARKGRAY = (64, 64, 64)
DARKGREEN = (0, 64, 0)
FUSCHIA = (255, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BGCOLOR = BLACK

WORMCOLOR = RED

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

startx = random.randint(5, CELLWIDTH - 6)
starty = random.randint(5, CELLHEIGHT - 6)

pygame.mixer.init()
nom = pygame.mixer.Sound("nom.wav")
death = pygame.mixer.Sound("death.wav")

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('COMIC.TTF', 18)
    pygame.display.set_caption('Snek')

    mainmenu()
    while True:
        options()
        runGame()
        showGameOverScreen()


def runGame():
    direction = RIGHT
    worm = WORM()
    tempFruitsNumber = fruitsNumber
    localWormSpeed = wormSpeed
    wormSpeedCounter = -1
    bomb = getRandomLocation()
    slowPowerupLoc = getRandomLocation()
    apples = []
    while tempFruitsNumber >= 1:
        apples.append(getRandomLocation())
        print(apples)
        tempFruitsNumber -= 1
    pygame.display.update()
    DISPLAYSURF.fill(BGCOLOR)
    drawGrid()
    worm.draw_worm()
    drawApples(apples)
    drawBomb(bomb)
    drawScore(len(worm.body) - 3)
    wormSpeedCounter = 30
    shouldDrawSlowPowerup = False
    slowPowerupTimer = 0

    while True: # main game loop
        a_KeyHasBeenPressed = False
        if wormSpeedCounter == 0:
            for event in pygame.event.get(): # event handling loop
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                        if a_KeyHasBeenPressed == False:
                            direction = LEFT
                            a_KeyHasBeenPressed = True
                    elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                        if a_KeyHasBeenPressed == False:
                            direction = RIGHT
                            a_KeyHasBeenPressed = True
                    elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                        if a_KeyHasBeenPressed == False:
                            direction = UP
                            a_KeyHasBeenPressed = True
                    elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                        if a_KeyHasBeenPressed == False:
                            direction = DOWN
                            a_KeyHasBeenPressed = True
                    elif event.key == K_ESCAPE:
                        terminate()

            # check if the worm has hit itself or the edge
            if not 0 <= worm.body[0].x < WINDOWWIDTH / CELLSIZE or not 0 <= worm.body[0].y < WINDOWWIDTH / CELLSIZE:
                return # game over
            
            for block in worm.body[1:]:
                if block == worm.body[0]:
                    return # game over

            # check if worm has eaten an apple
            eatenApples = 0
            for location in apples:
                if worm.body[0].x == location['x'] and worm.body[0].y == location['y']:
                    # don't remove worm's tail segment
                    appended = 0
                    while appended == 0:
                        loc = getRandomLocation()
                        if loc not in apples:
                            pygame.mixer.Sound.play(nom)
                            apples.remove(location)
                            apples.append(loc) # add a new apple
                            bomb = getRandomLocation()
                            appended = 1
                            worm.add_block()
                            eatenApples += 1
            
            # check if worm has eaten a Bomb
            if worm.body[0].x == bomb['x'] and worm.body[0].y == bomb['y']:
                return # game over
            
            # check if worm has eaten a Slow Powerup
            if shouldDrawSlowPowerup == True:
                if worm.body[0].x == slowPowerupLoc['x'] and worm.body[0].y == slowPowerupLoc['y']:
                    localWormSpeed = localWormSpeed // 2
                    slowPowerupTimer = 300

            # move the worm
            if direction == UP:
                worm.direction = Vector2(0,-1)
                worm.move_worm()
            elif direction == DOWN:
                worm.direction = Vector2(0,1)
                worm.move_worm()
            elif direction == LEFT:
                worm.direction = Vector2(-1,0)
                worm.move_worm()
            elif direction == RIGHT:
                worm.direction = Vector2(1,0)
                worm.move_worm()
            
            if slowModePowerups == True:
                if random.randint(1,300) == 300:
                    print("powerup should be drawn here")
                    shouldDrawSlowPowerup = True
            
            DISPLAYSURF.fill(BGCOLOR)
            drawGrid()
            worm.draw_worm()
            drawApples(apples)
            drawBomb(bomb)
            drawScore(len(worm.body) - 3)
            if shouldDrawSlowPowerup == True:
                drawSlowPowerup(slowPowerupLoc)
            wormSpeedCounter = localWormSpeed
        if shouldDrawSlowPowerup == True:
            if slowPowerupTimer >= 1:
                slowPowerupTimer -= 1
            elif slowPowerupTimer == 0:
                shouldDrawSlowPowerup = False
                slowPowerupTimer = -1
        wormSpeedCounter -= 1
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('COMIC.ttf', 100)
    titleSurf1 = titleFont.render('Snek!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Snek!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    pygame.mixer.Sound.play(death)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


class WORM():
    def __init__(self):
        #set worm starting location & vector
        self.body = [Vector2(startx, starty),
                     Vector2(startx - 1, starty),
                     Vector2(startx - 2, starty)]
        self.direction = Vector2(1,0)
        self.new_block = False
        self.change_color = WORMCOLOR

        self.load_graphics()
        self.scale_graphics()
        self.color_graphics()

    def load_graphics(self):
        #calls graphics into game
        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()

        self.eyes_up = pygame.image.load('graphics/eyes_up.png').convert_alpha()
        self.eyes_down = pygame.image.load('graphics/eyes_down.png').convert_alpha()
        self.eyes_right = pygame.image.load('graphics/eyes_right.png').convert_alpha()
        self.eyes_left = pygame.image.load('graphics/eyes_left.png').convert_alpha()

        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()

    def scale_graphics(self):
        #scale graphics to fit cell size
        self.head_up_scale = pygame.transform.smoothscale(self.head_up, (CELLSIZE, CELLSIZE))
        self.head_down_scale = pygame.transform.smoothscale(self.head_down, (CELLSIZE, CELLSIZE))
        self.head_right_scale = pygame.transform.smoothscale(self.head_right, (CELLSIZE, CELLSIZE))
        self.head_left_scale = pygame.transform.smoothscale(self.head_left, (CELLSIZE, CELLSIZE))

        self.eyes_up_scale = pygame.transform.smoothscale(self.eyes_up, (CELLSIZE, CELLSIZE))
        self.eyes_down_scale = pygame.transform.smoothscale(self.eyes_down, (CELLSIZE, CELLSIZE))
        self.eyes_right_scale = pygame.transform.smoothscale(self.eyes_right, (CELLSIZE, CELLSIZE))
        self.eyes_left_scale = pygame.transform.smoothscale(self.eyes_left, (CELLSIZE, CELLSIZE))

        self.tail_up_scale = pygame.transform.smoothscale(self.tail_up, (CELLSIZE, CELLSIZE))
        self.tail_down_scale = pygame.transform.smoothscale(self.tail_down, (CELLSIZE, CELLSIZE))
        self.tail_right_scale = pygame.transform.smoothscale(self.tail_right, (CELLSIZE, CELLSIZE))
        self.tail_left_scale = pygame.transform.smoothscale(self.tail_left, (CELLSIZE, CELLSIZE))

        self.body_vertical_scale = pygame.transform.smoothscale(self.body_vertical, (CELLSIZE, CELLSIZE))
        self.body_horizontal_scale = pygame.transform.smoothscale(self.body_horizontal, (CELLSIZE, CELLSIZE))

        self.body_tr_scale = pygame.transform.smoothscale(self.body_tr, (CELLSIZE, CELLSIZE))
        self.body_tl_scale = pygame.transform.smoothscale(self.body_tl, (CELLSIZE, CELLSIZE))
        self.body_br_scale = pygame.transform.smoothscale(self.body_br, (CELLSIZE, CELLSIZE))
        self.body_bl_scale = pygame.transform.smoothscale(self.body_bl, (CELLSIZE, CELLSIZE))

    def color_graphics(self):
        color_head_up = pygame.Surface(self.head_up_scale.get_size())
        color_head_down = pygame.Surface(self.head_down_scale.get_size())
        color_head_right = pygame.Surface(self.head_right_scale.get_size())
        color_head_left = pygame.Surface(self.head_left_scale.get_size())

        color_tail_up = pygame.Surface(self.tail_up_scale.get_size())
        color_tail_down = pygame.Surface(self.tail_down_scale.get_size())
        color_tail_right = pygame.Surface(self.tail_right_scale.get_size())
        color_tail_left = pygame.Surface(self.tail_left_scale.get_size())

        color_body_vertical = pygame.Surface(self.body_vertical_scale.get_size())
        color_body_horizontal = pygame.Surface(self.body_horizontal_scale.get_size())

        color_body_tr = pygame.Surface(self.body_tr_scale.get_size())
        color_body_tl = pygame.Surface(self.body_tl_scale.get_size())
        color_body_br = pygame.Surface(self.body_br_scale.get_size())
        color_body_bl = pygame.Surface(self.body_bl_scale.get_size())

        #apply the color to the graphics
        color_head_up.fill(self.change_color)
        color_head_down.fill(self.change_color)
        color_head_right.fill(self.change_color)
        color_head_left.fill(self.change_color)

        color_tail_up.fill(self.change_color)
        color_tail_down.fill(self.change_color)
        color_tail_right.fill(self.change_color)
        color_tail_left.fill(self.change_color)

        color_body_vertical.fill(self.change_color)
        color_body_horizontal.fill(self.change_color)

        color_body_tr.fill(self.change_color)
        color_body_tl.fill(self.change_color)
        color_body_br.fill(self.change_color)
        color_body_bl.fill(self.change_color)

        #apply blend to graphic
        self.head_up_color = self.head_up_scale.copy()
        self.head_up_color.blit(color_head_up, (0, 0), special_flags = pygame.BLEND_MULT)
        self.head_down_color = self.head_down_scale.copy()
        self.head_down_color.blit(color_head_down, (0, 0), special_flags = pygame.BLEND_MULT)
        self.head_right_color = self.head_right_scale.copy()
        self.head_right_color.blit(color_head_right, (0, 0), special_flags = pygame.BLEND_MULT)
        self.head_left_color = self.head_left_scale.copy()
        self.head_left_color.blit(color_head_left, (0, 0), special_flags = pygame.BLEND_MULT)

        self.tail_up_color = self.tail_up_scale.copy()
        self.tail_up_color.blit(color_tail_up, (0, 0), special_flags = pygame.BLEND_MULT)
        self.tail_down_color = self.tail_down_scale.copy()
        self.tail_down_color.blit(color_tail_down, (0, 0), special_flags = pygame.BLEND_MULT)
        self.tail_right_color = self.tail_right_scale.copy()
        self.tail_right_color.blit(color_tail_right, (0, 0), special_flags = pygame.BLEND_MULT)
        self.tail_left_color = self.tail_left_scale.copy()
        self.tail_left_color.blit(color_tail_left, (0, 0), special_flags = pygame.BLEND_MULT)

        self.body_vertical_color = self.body_vertical_scale.copy()
        self.body_vertical_color.blit(color_body_vertical, (0, 0), special_flags = pygame.BLEND_MULT)
        self.body_horizontal_color = self.body_horizontal_scale.copy()
        self.body_horizontal_color.blit(color_body_horizontal, (0, 0), special_flags = pygame.BLEND_MULT)

        self.body_tr_color = self.body_tr_scale.copy()
        self.body_tr_color.blit(color_body_tr, (0, 0), special_flags = pygame.BLEND_MULT)
        self.body_tl_color = self.body_tl_scale.copy()
        self.body_tl_color.blit(color_body_tl, (0, 0), special_flags = pygame.BLEND_MULT)
        self.body_br_color = self.body_br_scale.copy()
        self.body_br_color.blit(color_body_br, (0, 0), special_flags = pygame.BLEND_MULT)
        self.body_bl_color = self.body_bl_scale.copy()
        self.body_bl_color.blit(color_body_bl, (0, 0), special_flags = pygame.BLEND_MULT)
    
    def draw_worm(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index,block in enumerate(self.body):
            #rect for positioning
            x_pos = int(block.x * CELLSIZE)
            y_pos = int(block.y * CELLSIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELLSIZE, CELLSIZE)

            #worm direction
            if index == 0:
                DISPLAYSURF.blit(self.head,block_rect)
                DISPLAYSURF.blit(self.eyes,block_rect)
            elif index == len(self.body) -1:
                DISPLAYSURF.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index +1] - block
                next_block = self.body[index -1] - block
                if previous_block.x == next_block.x:
                    DISPLAYSURF.blit(self.body_vertical_color,block_rect)
                elif previous_block.y == next_block.y:
                    DISPLAYSURF.blit(self.body_horizontal_color,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        DISPLAYSURF.blit(self.body_tl_color,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        DISPLAYSURF.blit(self.body_bl_color,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        DISPLAYSURF.blit(self.body_tr_color,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        DISPLAYSURF.blit(self.body_br_color,block_rect)

    def update_head_graphics(self):
        #determine head & eyes graphic direction
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left_color
            self.eyes = self.eyes_left_scale
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right_color
            self.eyes = self.eyes_right_scale
        elif head_relation == Vector2(0,1):
            self.head = self.head_up_color
            self.eyes = self.eyes_up_scale
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down_color
            self.eyes = self.eyes_down_scale

    def update_tail_graphics(self):
        #determine tail graphics direction
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left_color
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right_color
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up_color
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down_color

    def move_worm(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

def drawApples(coords):
    apple_graph = pygame.image.load('graphics/apple_red.png').convert_alpha()
    appleAdj = pygame.transform.smoothscale(apple_graph, (CELLSIZE, CELLSIZE))
    for coord in coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        DISPLAYSURF.blit(appleAdj, appleRect)
    
def drawBomb(coord):
    bomb_graph = pygame.image.load('graphics/bomb.png').convert_alpha()
    bombAdj = pygame.transform.smoothscale(bomb_graph, (CELLSIZE, CELLSIZE))
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    bombRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    DISPLAYSURF.blit(bombAdj, bombRect)
    
def drawSlowPowerup(coord):
    gold_graph = pygame.image.load('graphics/apple_gold.png').convert_alpha()
    goldAdj = pygame.transform.smoothscale(gold_graph, (CELLSIZE, CELLSIZE))
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    powerupRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    DISPLAYSURF.blit(goldAdj, powerupRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def options():
    global fruitsNumber, wormSpeed, wormInnerColor, wormOuterColor, slowModePowerups
    wormInnerColor = BLACK
    wormOuterColor = BLUE
    fruitsNumber = 100
    wormSpeed = 2
    slowModePowerups = False
    return

def mainmenu():
    titleFont = pygame.font.Font('COMIC.ttf', 100)
    titleSurf1 = titleFont.render('Snek!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Snek!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 1.5 # rotate by 1.5 degrees each frame
        degrees2 += 3.5 # rotate by 3.5 degrees each frame

if __name__ == '__main__':
    main()
