'''
Project initiation date: December 22 2017
Author: Wouter Haaxman
Regarding project code: Copyright 2017, Wouter Haaxman, All rights reserved.
'''

import sys
import pygame
from pygame.locals import *

#=====================================CLASSES=================================
display_pixel_width = 600
display_pixel_height = 600

class Soldier(pygame.sprite.Sprite):
    """ This is the soldier class """
    def __init__(self):
        super().__init__()
        #Create soldier sprite.
        self.image = pygame.image.load('ball_black.png').convert()

        #Blit the image surface on the game surface.
        self.rect = self.image.get_rect()
        self.x = int(display_pixel_width/2)
        self.y = int(display_pixel_height/2)
        DISPLAYSURF.blit(self.image, (self.x, self.y))


class Bullet(pygame.sprite.Sprite):
    """ This is the bullet class """
    def __init__(self):
        super().__init__()

        self.x = int(display_pixel_width/2)
        self.y = int(display_pixel_height/2)
        #Create soldier sprite and resize it.
        self.image = pygame.image.load('ball_black.png')#.convert()
        self.size = self.image.get_size() # return a width and height of the image
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.05), int(self.size[1]*0.05)))
        #Blit the image surface on the game surface.
        DISPLAYSURF.blit(self.image, (self.x, self.y))

#============================================================================


pygame.init()       #Initialize pygame module (required before calling any pygame stuff)
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
#==============DEFINE COLORs================================================
color_black = pygame.Color(0,0,0,255)
color_white = pygame.Color(255, 255, 255)
color_red = pygame.Color(255,0,0)
color_green = pygame.Color(0,255,0)
color_blue = pygame.Color(0,0,255)

#==============DEFINE DISPLAY SCREEN======================================
DISPLAYSURF = pygame.display.set_mode((display_pixel_width,display_pixel_height))
pygame.display.set_caption('Freedom')

#set background of the display surface to white and draw circle in middle
DISPLAYSURF.fill(color_white)

soldier1 = Soldier()

#pygame.draw.circle(DISPLAYSURF, color_black, (soldier1.x, soldier1.y), soldier1.pixel_radius, 0)
#=================MAIN GAME LOOP===============================================
while True:
    #Event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #Events handled and possibly game state changed: update display accordingly
    pygame.display.update()
    fpsClock.tick(FPS)
