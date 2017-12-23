'''
Project initiation date: December 22 2017
Author: Wouter Haaxman
Regarding project code: Copyright 2017, Wouter Haaxman, All rights reserved.

useful links (used/tweaked parts to implement here):
https://www.pygame.org/docs
http://programarcadegames.com/python_examples/f.php?file=bullets.py
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
        self.image = pygame.image.load('images/ball_black.png').convert() #image object is a surfaceS

        self.rect = self.image.get_rect()
        self.rect.centerx = int(display_pixel_width/2)
        self.rect.centery = int(display_pixel_height/2)

    def update(self):
        pass


class Bullet(pygame.sprite.Sprite):
    """ This is the bullet class """
    def __init__(self):
        super().__init__()

        #Create soldier sprite and resize it.
        self.image = pygame.image.load('images/ball_black.png')#.convert()
        self.size = self.image.get_size() # return a width and height of the image
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.2), int(self.size[1]*0.2)))

        self.rect = self.image.get_rect()


    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3

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
BACKGROUND_SURFACE = pygame.display.set_mode((display_pixel_width,display_pixel_height))
pygame.display.set_caption('Freedom')

#set background of the display surface to white and draw circle in middle
BACKGROUND_SURFACE.fill(color_white)

#initialize bullet list which is update in event handler.
all_sprites_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
#Add soldier and put in sprites list
soldier1 = Soldier()
all_sprites_list.add(soldier1)

#pygame.draw.circle(BACKGROUND_SURFACE, color_black, (soldier1.x, soldier1.y), soldier1.pixel_radius, 0)
#=================MAIN GAME LOOP===============================================
while True:
    #Event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            #print(pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0] == 1: # (left mb,right mb, scroller?) -> (0/1,0/1,?)
                bullet = Bullet()
                # Set the bullet so it is where the player is
                bullet.rect.x = soldier1.rect.x
                bullet.rect.y = soldier1.rect.y
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
                print('SHOOT')

    all_sprites_list.update() # This is a nice feature to quickly call the update()
    #method for all of the sprites in this list.

    # Calculate bullet trajectories (to come soon)
    for bullet in bullet_list:
        # Remove the bullet when out of bounds
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)


    BACKGROUND_SURFACE.fill(color_white)# Clear the screen
    all_sprites_list.draw(BACKGROUND_SURFACE)# Draw all the spites

    #Events handled and possibly game state changed: update display accordingly
    pygame.display.flip()# Go ahead and update the screen with what we've drawn.
    fpsClock.tick(FPS)
