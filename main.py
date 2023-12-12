# the following are necessary modules.
import random  # for generating random height of pipes
import sys  # sys.exit from sys module will be used to exit the game
import pygame  # as recommended by Anastasia, importing pygame module to get a nice GUI
from pygame.locals import * #bacis pygame imports

FPS = 32  # frames per second,it’s just the game of removing images and blitting new ones, but it happens 32 times a second
# setting screen width and height
screenwidth = 289
screenheight = 511
screen = pygame.display.set_mode((screenwidth, screenheight))
ground = screenheight * 0.8  # base image
pics = {}
sounds = {}
bird = 'resources/pics/bird.png'
background = 'resources/pics/background.jpg'
pipe = 'resources/pics/pipe.png'


def welcomescreen(): #welcome screen
    
    birdx = int(screenwidth / 5) #to place the bird on the left side
    birdy = int((screenheight - pics['bird'].get_height()) / 2) #to place the bird at the centre in y axis
    messagex = int((screenwidth - pics['message'].get_width()) / 2) #to display message pic at the centre
    messagey = int(screenheight * 0.13) #y-coordinate of the message pic
    basex = 0 # x-coord... of the base image (for y-coord..., its already declared in global variables named as ground)
    playbutton = pygame.Rect(108, 222, 68, 65) #rectangle for playbutton
    pygame.mixer.music.load('resources/sounds/intromusic.mp3') # intro music
    pygame.mixer.music.play()

    # while loop to avoid our screen disappear within 1/32th of a second. With this loop screen will be refreshed.
    while True:
        for event in pygame.event.get():
            
            # Close the game when user clicks on Cross or presses the Escape button
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            # Start the game when user presses the Space bar or up arrow key
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
                
            # Start the game when mouse cursor clicks on play button
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


# It's the main function to play the actual game
def mainGame():
    
    #to load background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load('resources/sounds/backgroundmusic.mp3')
    pygame.mixer.music.play()
    score = 0
    birdx = int(screenwidth / 5)
    birdy = int(screenheight / 2)
    basex = 0

    #creating upper and lower pipes for the game
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #upper pipes list
    upperPipes = [
        {'x': screenwidth + 200, 'y': newPipe1[0]['y']},
        {'x': screenwidth + 200 + (screenwidth / 2), 'y': newPipe2[0]['y']}
    ]

    #lower pipes list
    lowerPipes = [
        {'x': screenwidth + 200, 'y': newPipe1[1]['y']},
        {'x': screenwidth + 200 + (screenwidth / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4 #to move our pipe from right to left not left to right
    birdVelY = -9 #between bird's max and min velocity
    birdMaxVelY = 10
    birdMinVelY = -8
    birdAccY = 1

    birdFlapAccv = -10 #velocity while flapping
    birdFlapped = False #true only when bird is flapping

    while True:

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #to check if the user has pressed the Space bar key or up arrow key,
            #and if birdY is greater that 0 then update the bird's y velocity with bird's velocity while flapping
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if birdy > 0:
                    birdVelY = birdFlapAccv
                    birdFlapped = True #change the boolean value to true from false that the bird is flapped
                    sounds['wing'].play() #play the sound effect

        #check for score
        birdMidPos = birdx + pics['bird'].get_width() / 2 #to obtain mid-position of the bird and pipe
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + pics['pipe'][0].get_width() / 2
            #if the mid-position of the bird crosses the mid-position of the pipe, then increase the score by 1
            if pipeMidPos <= birdMidPos < pipeMidPos + 4:
                score += 1
                #print the score and play the sound effect
                print(f"Score is {score}")
                sounds['point'].play()

        if birdVelY < birdMaxVelY and not birdFlapped:
            birdVelY += birdAccY

        #if bird touches the ground, don't go further than that and set value of the birdY to birdY
        if birdFlapped:
            birdFlapped = False
        birdHeight = pics['bird'].get_height()
        birdy = birdy + min(birdVelY, ground - birdy - birdHeight) #value will become zero

        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        #add a new pipe when the first one is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #if the pipe is out of screen, remove it
        if upperPipes[0]['x'] < -pics['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #to refresh pics
        screen.blit(pics['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(pics['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(pics['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(pics['base'], (basex, ground))
        screen.blit(pics['bird'], (birdx, birdy))

        #to show the score on the screen
        Scores = [int(x) for x in list(str(score))] #creating a list to store the scores
        width = 0 #first set the width to zero
        for digit in Scores: #create a loop for our digits and then increase the width with the pics, width for numbers
            width += pics['numbers'][digit].get_width()
        Xoffset = (screenwidth - width) / 2 #X-coordinate where the scores will be shown

        for digit in Scores:
            screen.blit(pics['numbers'][digit], (Xoffset, screenheight * 0.12))
            Xoffset += pics['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        # returns true if the bird is crashed and then will return the hit function
        # and will check which collision is happened and then will follow the further statement
        hitTest = hit(birdx, birdy, upperPipes, lowerPipes)
        if hitTest:
            return


#to generate random upper and lower pipes
def getRandomPipe():
    """
    generating positions of the two pipes one upper pipe and other lower pipe
    """

    pipeHeight = pics['pipe'][0].get_height()
    offset = screenheight / 3.5 #to create a gap between two pipes to pass the bird
    # random.range function generates random values between ranges
    y2 = offset + random.randrange(0, int(screenheight - pics['base'].get_height() - 1.2 * offset))
    pipeX = screenwidth + 10 #x of both pipes will be same.
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper pipes
        {'x': pipeX, 'y': y2}  # lower pipes
    ]
    return pipe


#to check if the bird hit the pipes or not
def hit(birdx, birdy, upperPipes, lowerPipes):

    #collision with the ground
    #check if the birds Y-coordinate has become greater that ground - 29, or if the Y-coordinate is smaller than 0
    if birdy > ground - 29 or birdy < 0:
        #then play hit sound effect, and call gameOver function
        sounds['hit'].play()
        gameOver()

    #upper pipe collision
    for pipe in upperPipes:
        # get pipe height and then check if birdy is smaller than the sum of the pipe height and y
        pipeHeight = pics['pipe'][0].get_height()
        # then check if the absolute value of the difference of bird x
        # and pipe x is smaller than the upper pipe's width -20
        if birdy < pipeHeight + pipe['y'] and abs(birdx - pipe['x']) < pics['pipe'][0].get_width() - 20:
            #if yes, play hit sound effect and call gameOver function
            sounds['hit'].play()
            print(birdx, pipe['x'],)
            gameOver()

    #lower pipe collision
    for pipe in lowerPipes:
        #same as upper pipe collision
        if birdy + pics['bird'].get_height() > pipe['y'] and abs(birdx - pipe['x']) < pics['pipe'][0].get_width() - 20:
            sounds['hit'].play()
            gameOver()

    return False

#game over function, we should have images related and then will give the player a choice to either retry or go home
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

            #Quit game if escape key is pressed
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #replay if space key bar is pressed
            if event.type == KEYDOWN and event.key == K_SPACE:
                mainGame()

            #retry button
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            #if mouse cursor's x-coordinate is greater than 30 and less than the width of the button
            if 30 < pygame.mouse.get_pos()[0] < 30 + pics['retry'].get_width():
                #check if the cursor's y-coordinate is greater than 220 and less than 220 + height of the button
                if 220 < pygame.mouse.get_pos()[1] < 220 + pics['retry'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    #if mouse is pressed
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        #replay the game by calling main game function
                        mainGame()

            #home button
            if 30 < pygame.mouse.get_pos()[0] < 30 + pics['home'].get_width():
                if 280 < pygame.mouse.get_pos()[1] < 280 + pics['home'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        #return to the welcome screen
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
