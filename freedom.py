'''
Project initiation date: December 22 2017
Author: Wouter Haaxman
Regarding project code: Copyright 2017, Wouter Haaxman, All rights reserved.

useful links (used/tweaked parts to implement here):
https://www.pygame.org/docs
http://programarcadegames.com/python_examples/f.php?file=bullets.py
https://www.soundjay.com/gun-sound-effect.html(source of gunshot sound)
https://www.youtube.com/watch?v=3RJx34kGRGk (start menu tutorial)
https://www.youtube.com/watch?v=jh_m-Eytq0Q (buttons in start menu)
https://images.fineartamerica.com/images-medium-large/lieutenant-general-george-patton-left-everett.jpg (image patton)

'''

import sys
import math
import pygame
from pygame.locals import *

#=====================================CLASSES=================================
display_pixel_width = 700
display_pixel_height = 546

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

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

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

def createButton(btn_text, pos_tuple, inact_color, act_color):
    '''
    This function creates a button on the BACKGROUND_SURFACE.
    When mouse hoovers over the button it can change color

    The function returns 1/0 depending on whether or not mouse is on btn.

    btn_Text: text displayed inside the button.
    pos_tuple: (x,y,width,height).
    inact_color: color when button is inactive.
    act_color: color when button is active (moused over)

    '''
    rect_btn = pygame.draw.rect(BACKGROUND_SURFACE, inact_color, pos_tuple)
    #interact with buttons:
    mouse = pygame.mouse.get_pos()
    if rect_btn.collidepoint(mouse) == 1:
        pygame.draw.rect(BACKGROUND_SURFACE, act_color, pos_tuple) #redraw

    #Put text inside the start and quit "buttons"
    smallText = pygame.font.Font('freesansbold.ttf',20)
    text_surf_btn, text_rect_btn = text_objects(btn_text, smallText)
    text_rect_btn.center = (rect_btn.centerx,rect_btn.centery)
    BACKGROUND_SURFACE.blit(text_surf_btn, text_rect_btn) # Actually draw(blit) it.

    return rect_btn.collidepoint(mouse)

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
inact_color_start_Btn = pygame.Color(200,200,200)
inact_color_quit_Btn = pygame.Color(200,200,200)
act_color_start_Btn = pygame.Color(100,100,100)
act_color_quit_Btn = pygame.Color(100,100,100)

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

#=====================START MENU============================================
def text_objects(text, font):
    textSurface = font.render(text, True, color_white)
    return textSurface, textSurface.get_rect()

def start_menu():
    hold_menu = True
    while hold_menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        BackGround = Background('images/gen_troops.png', [0,0])
        BACKGROUND_SURFACE.fill([255, 255, 255])
        BACKGROUND_SURFACE.blit(BackGround.image, BackGround.rect)
        #BACKGROUND_SURFACE.fill(color_blue)

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects('Freedom', largeText)
        TextRect.center = ((display_pixel_width/2) , (display_pixel_height/2))
        BACKGROUND_SURFACE.blit(TextSurf, TextRect)
        #Draw and interact with the start and quit buttons:
        pos_start_Btn = ((display_pixel_width/3)-40,(display_pixel_height/1.4),100,50)
        pos_quit_Btn = (2*(display_pixel_width/3)-40,(display_pixel_height/1.4),100,50)

        #createButton(btn_text, pos_tuple, inact_color, act_color):
        mouse_on_start = createButton('Start',pos_start_Btn, act_color_start_Btn, inact_color_start_Btn)
        mouse_on_quit = createButton('Quit', pos_quit_Btn, act_color_quit_Btn, inact_color_quit_Btn)

        if mouse_on_start and pygame.mouse.get_pressed()[0] == 1:
            game_loop()
        if mouse_on_quit and pygame.mouse.get_pressed()[0] == 1:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)


#pygame.draw.circle(BACKGROUND_SURFACE, color_black, (soldier1.x, soldier1.y), soldier1.pixel_radius, 0)
#=================MAIN GAME LOOP===============================================
def game_loop():
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

start_menu()
game_loop()
