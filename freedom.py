'''
Project initiation date: December 22 2017
Author: Wouter Haaxman
Regarding project code: Copyright 2017, Wouter Haaxman, All rights reserved.

useful links (used/tweaked parts to implement here):
https://www.pygame.org/docs
http://programarcadegames.com/python_examples/f.php?file=bullets.py
https://www.soundjay.com/gun-sound-effect.html(source of gunshot sound)
'''

import sys
import math
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
        self.rect.x = soldier1.rect.x
        self.rect.y = soldier1.rect.y
        self.mousex = pygame.mouse.get_pos()[0]
        self.mousey = pygame.mouse.get_pos()[1]

        self.dx = self.mousex - self.rect.centerx
        self.dy = self.mousey - self.rect.centery
        self.length = math.sqrt( self.dx**2 + self.dy**2 )
        self.factor = 10
        '''
        print('=====')
        print('length = ' + str(self.length))
        print('dx ' + str(self.factor*(self.dx/self.length)))
        print('dy ' + str(self.factor*(self.dy/self.length)))
        print('=====')
        '''

    def update(self):
        """ Move the bullet. """

        self.rect.x += self.factor*(self.dx/self.length)
        self.rect.y += self.factor*(self.dy/self.length)


#=================================FUNCTIONS=====================================
def createBullet():
    bullet = Bullet()
    sound_gunshot = pygame.mixer.Sound('sounds/gunshot.ogg')
    sound_gunshot.play()
    # Set the bullet so it is where the player is
    bullet.rect.x = soldier1.rect.x
    bullet.rect.y = soldier1.rect.y
    # Add the bullet to the lists
    all_sprites_list.add(bullet)
    bullet_list.add(bullet)

#=============================INITIALIZATION=====================================
pygame.init()       #Initialize pygame module (required before calling any pygame stuff
#pygame.mixer.music.load('sounds/musicfile_here.mp3') #Background music
#pygame.mixer.music.play(loops = -1 ,start = 0.0)#-1 : inifinite loop
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
                print('draw box')
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                createBullet()

    all_sprites_list.update() # This is a nice feature to quickly call the update()
    #method for all of the sprites in this list.

    for bullet in bullet_list:
        # Remove the bullet when out of bounds
        if bullet.rect.y < -5 or bullet.rect.x < -5:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)


    BACKGROUND_SURFACE.fill(color_white)# Clear the screen
    all_sprites_list.draw(BACKGROUND_SURFACE)# Draw all the sprites

    #Events handled and possibly game state changed: update display accordingly
    pygame.display.flip()# Go ahead and update the screen with what we've drawn.
    fpsClock.tick(FPS)
