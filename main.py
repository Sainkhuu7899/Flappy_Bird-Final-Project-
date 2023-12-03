# the following are necessary modules.
import random  # for generating random height of pipes
import sys  # sys.exit from sys module will be used to exit the game
import pygame  # as recommended by Anastasia, importing pygame module to get a nice GUI
from pygame.locals import *

FPS = 32  # frames per second
# setting screen width and height
screenwidth = 289
screenheight = 511
screen = pygame.display.set_mode((screenwidth, screenheight))
ground = screenheight * 0.8  # base image
pics = {}
sounds = {}
bird = 'resources/pics/bird.png'
background = 'resources/pics/background.jpeg'
pipe = 'resources/pics/pipe.png'


def welcomescreen():
    birdx = int(screenwidth / 5)
    birdy = int((screenheight - pics['bird'].get_height()) / 2)
    messagex = int((screenwidth - pics['message'].get_width()) / 2)
    messagey = int(screenheight * 0.13)
    basex = 0
    #rectangle for playbutton
    playbutton = pygame.Rect(108, 222, 68, 65)
    # intro music
    pygame.mixer.music.load('resources/sounds/intromusic.mp3')
    pygame.mixer.music.play()

    while True:
        for event in pygame.event.get():
            # Close the game when user clicks on Cross or presses the Escape button
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pos()[0] > playbutton[0] and pygame.mouse.get_pos()[0] < playbutton[0] + playbutton[2]:
                if pygame.mouse.get_pos()[1] > playbutton[1] and pygame.mouse.get_pos()[1] < playbutton[1] + playbutton[3]:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if playbutton.collidepoint(pygame.mouse.get_pos()):  # checking if mouse is collided with the play button

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # checking if mouse has been clicked
                        mainGame()
        else:
            screen.blit(pics['background'], (0, 0))
            screen.blit(pics['bird'], (birdx, birdy))
            screen.blit(pics['message'], (messagex, messagey))
            screen.blit(pics['base'], (basex, ground))

            pygame.display.update()
            FPSCLOCK.tick(FPS)

def mainGame():
    #background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load('resources/sounds/backgroundmusic.mp3')
    pygame.mixer.music.play()
    score = 0
    birdx = int(screenwidth / 5)
    birdy = int(screenheight / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': screenwidth + 200, 'y': newPipe1[0]['y']},
        {'x': screenwidth + 200 + (screenwidth / 2), 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': screenwidth + 200, 'y': newPipe1[1]['y']},
        {'x': screenwidth + 200 + (screenwidth / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4
    birdVelY = -9
    birdMaxVelY = 10
    birdMinVelY = -8
    birdAccY = 1

    birdFlapAccv = -10
    birdFlapped = False

    while True:

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if birdy > 0:
                    birdVelY = birdFlapAccv
                    birdFlapped = True
                    sounds['wing'].play()

        hitTest = hit(birdx, birdy, upperPipes, lowerPipes)
        if hitTest:
            return

        birdMidPos = birdx + pics['bird'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + pics['pipe'][0].get_width() / 2
            if pipeMidPos <= birdMidPos < pipeMidPos + 4:
                score += 1
                print(f"Score is {score}")
                sounds['point'].play()

        if birdVelY < birdMaxVelY and not birdFlapped:
            birdVelY += birdAccY

        if birdFlapped:
            birdFlapped = False
        birdHeight = pics['bird'].get_height()
        birdy = birdy + min(birdVelY, ground - birdy - birdHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -pics['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        screen.blit(pics['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(pics['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(pics['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(pics['base'], (basex, ground))
        screen.blit(pics['bird'], (birdx, birdy))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += pics['numbers'][digit].get_width()
        Xoffset = (screenwidth - width) / 2

        for digit in myDigits:
            screen.blit(pics['numbers'][digit], (Xoffset, screenheight * 0.12))
            Xoffset += pics['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def hit(birdx, birdy, upperPipes, lowerPipes):
    if birdy > ground - 25 or birdy < 0:
        sounds['hit'].play()
        gameOver()

    for pipe in upperPipes:
        pipeHeight = pics['pipe'][0].get_height()
        if birdy < pipeHeight + pipe['y'] and abs(birdx - pipe['x']) < pics['pipe'][0].get_width() - 20:
            sounds['hit'].play()
            print(birdx, pipe['x'],)
            gameOver()

    for pipe in lowerPipes:
        if birdy + pics['bird'].get_height() > pipe['y'] and abs(birdx - pipe['x']) < pics['pipe'][0].get_width() - 20:
            sounds['hit'].play()
            gameOver()

    return False


def getRandomPipe():
    pipeHeight = pics['pipe'][0].get_height()
    offset = screenheight / 3.5
    y2 = offset + random.randrange(0, int(screenheight - pics['base'].get_height() - 1.2 * offset))
    pipeX = screenwidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper pipes
        {'x': pipeX, 'y': y2}  # lower pipes
    ]
    return pipe


def gameOver():
    screen = pygame.display.set_mode((screenwidth, screenheight))
    pygame.display.set_caption('Flappy Bird by Sainkhuu')
    pics['over'] = pygame.image.load('resources/pics/gameover.png').convert_alpha()
    pics['retry'] = pygame.image.load('resources/pics/retry.png').convert_alpha()
    pics['home'] = pygame.image.load('resources/pics/home.png').convert_alpha()
    screen.blit(pics['background'], (0, 0))
    screen.blit(pics['base'], (0, ground))
    screen.blit(pics['over'], (0, 0))
    screen.blit(pics['retry'], (30, 220))
    screen.blit(pics['home'], (30, 280))
    pygame.display.update()

    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                mainGame()
            #retry button
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if 30 < pygame.mouse.get_pos()[0] < 30 + pics['retry'].get_width():
                if 220 < pygame.mouse.get_pos()[1] < 220 + pics['retry'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mainGame()
            #home button
            if 30 < pygame.mouse.get_pos()[0] < 30 + pics['home'].get_width():
                if 280 < pygame.mouse.get_pos()[1] < 280 + pics['home'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        welcomescreen()

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


if __name__ == "__main__":
    pygame.init()  # initializing the modules of pygame
    FPSCLOCK = pygame.time.Clock()  # for controlling FPS (refresh rate)
    pygame.display.set_caption('Flappy Bird by Sainkhuu')

    # Loading pictures
    pics['numbers'] = (
        pygame.image.load('resources/pics/0.png').convert_alpha(),
        pygame.image.load('resources/pics/1.png').convert_alpha(),
        pygame.image.load('resources/pics/2.png').convert_alpha(),
        pygame.image.load('resources/pics/3.png').convert_alpha(),
        pygame.image.load('resources/pics/4.png').convert_alpha(),
        pygame.image.load('resources/pics/5.png').convert_alpha(),
        pygame.image.load('resources/pics/6.png').convert_alpha(),
        pygame.image.load('resources/pics/7.png').convert_alpha(),
        pygame.image.load('resources/pics/8.png').convert_alpha(),
        pygame.image.load('resources/pics/9.png').convert_alpha(),
    )
    pics['background'] = pygame.image.load(background).convert_alpha()
    pics['base'] = pygame.image.load('resources/pics/base.png').convert_alpha()
    pics['bird'] = pygame.image.load(bird).convert_alpha()
    pics['message'] = pygame.image.load('resources/pics/message.png').convert_alpha()
    pics['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )

    # game sounds
    sounds['hit'] = pygame.mixer.Sound('resources/sounds/hit.mp3')
    sounds['point'] = pygame.mixer.Sound('resources/sounds/point.mp3')
    sounds['wing'] = pygame.mixer.Sound('resources/sounds/wing.wav')
    sounds['intromusic'] = pygame.mixer.Sound('resources/sounds/intromusic.mp3')

while True:
    welcomescreen()
    mainGame()
