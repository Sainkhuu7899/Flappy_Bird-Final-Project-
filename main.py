import random # for generating random height of pipes
import sys # sys.exit from sys module will be used to exit the game
import pygame # as recommended by Anastasia, importing pygame module to get a nice GUI
from pygame.locals import *

FPS = 32 # frames per second
# setting screen width and height
screenwidth = 289
screenheight = 511
screen = pygame.display.set_mode((screenwidth, screenheight))
ground = screenheight*0.8 #base image
pics = {}
sounds = {}
bird = 'resources\pics\\bird.png'
background = 'resources\pics\\background.jpeg'
pipe = 'resources\pics\\pipe.png'

def welcomescreen():

    playerx = int(screenwidth/5)
    playery = int(screenheight - pics['bird'].get_height())/2
    messagex = int(screenwidth - pics['message'].get_width)/2
    messagey = int(screenheight * 0.13)
    basex = 0

if __name__ == "__main__":
    pygame.init() #initializing the modules of pygame
    fpsclock = pygame.time.Clock() #for controlling FPS (refresh rate)

    #Loading pictures
    pics['numbers'] = (
        pygame.image.load('resources\pics\\0.png').convert_alpha(),
        pygame.image.load('resources\pics\\1.png').convert_alpha(),
        pygame.image.load('resources\pics\\2.png').convert_alpha(),
        pygame.image.load('resources\pics\\3.png').convert_alpha(),
        pygame.image.load('resources\pics\\4.png').convert_alpha(),
        pygame.image.load('resources\pics\\5.png').convert_alpha(),
        pygame.image.load('resources\pics\\6.png').convert_alpha(),
        pygame.image.load('resources\pics\\7.png').convert_alpha(),
        pygame.image.load('resources\pics\\8.png').convert_alpha(),
        pygame.image.load('resources\pics\\9.png').convert_alpha(),
    )
    pics['background'] = pygame.image.load(background).convert_alpha
    pics['bird'] = pygame.image.load(bird).convert_alpha
    pics['message'] = pygame.image.load('resources\pics\\base.png').convert_alpha
    pics['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), #upper pipes are just the pipes rotated by 180 degrees
    pygame.image.load(PIPE).convert_alpha() #lower pipes
    )
