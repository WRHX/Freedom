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

#=============some constant declaration or initiation=================
display_pixel_width = 700
display_pixel_height = 546
initial_xy = None
#=====================================CLASSES=================================

class Soldier(pygame.sprite.Sprite):
    """ This is the soldier class """
    def __init__(self):
        super().__init__()
        #Create soldier sprite.
        self.image = pygame.image.load('images/unit_unselected.png').convert() #image object is a surfaceS

        self.rect = self.image.get_rect()
        self.rect.centerx = int(display_pixel_width/2)
        self.rect.centery = int(display_pixel_height/2)

        self.is_selected = 0 # Used in the unitSelection function. Enabling movement & weapons.

    def update(self):
        pass


class Bullet(pygame.sprite.Sprite):
    """ This is the bullet class """
    def __init__(self):
        super().__init__()

        #Create soldier sprite and resize it.
        self.image = pygame.image.load('images/bullet.png')#.convert()
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
def createBullets():
    for unit in unit_list:
        if unit.is_selected:
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
    text_surf_btn, text_rect_btn = text_objects(btn_text, smallText, color_white)
    text_rect_btn.center = (rect_btn.centerx,rect_btn.centery)
    BACKGROUND_SURFACE.blit(text_surf_btn, text_rect_btn) # Actually draw(blit) it.

    return rect_btn.collidepoint(mouse)

def getCoordinatesOfTopLeftCorner(x_i,y_i,x_m,y_m):
    '''
    To be commented
    Find top left coordinates (surface requires these coordinates)
    '''
    if x_m - x_i > 0 and y_m - y_i > 0:
        x_tl = x_i
        y_tl = y_i
    elif x_m - x_i < 0 and y_m - y_i > 0:
        x_tl = x_m
        y_tl = y_i
    elif x_m - x_i > 0 and y_m - y_i < 0:
        x_tl = x_i
        y_tl = y_m
    elif x_m - x_i < 0 and y_m - y_i < 0:
        x_tl = x_m
        y_tl = y_m
    else:
        x_tl = x_i
        y_tl = x_i

    return x_tl,y_tl

def drawSelectionBox(initial_xy):
    '''
    To be commented
    '''
    if initial_xy != None and pygame.mouse.get_pressed()[0] == 1:
        x_i = initial_xy[0] # x-coord. at time of mousebuttondown
        y_i = initial_xy[1] # y-coord at time of mousebuttondown
        x_m = pygame.mouse.get_pos()[0] # current x-coord. of mouse (still pressed)
        y_m = pygame.mouse.get_pos()[1] # current y-coord. of mouse (still pressed)
        xy_list = [x_i,y_i,x_m,y_m]


        # non-functional but visible selection box (borders only)
        # Create a total rectangle made up of 4 rectangles (cleaner draw in pygame)
        pygame.draw.rect(BACKGROUND_SURFACE, color_green, pygame.Rect(x_i, y_i, (x_m-x_i), 1)) #Top of total rectangle
        pygame.draw.rect(BACKGROUND_SURFACE, color_green, pygame.Rect(x_i, y_i, 1, (y_m-y_i))) #Left of total rectangle
        pygame.draw.rect(BACKGROUND_SURFACE, color_green, pygame.Rect(x_m, y_i, 1, (y_m-y_i)))
        pygame.draw.rect(BACKGROUND_SURFACE, color_green, pygame.Rect(x_i, y_m, (x_m-x_i), 1))
        # Create a transparent green area within the rectangle defined above:
        try:
            SelBox_surface = pygame.Surface((int(math.fabs(x_m-x_i)),int(math.fabs(y_m-y_i)))) # Make a new surface of which we can change transparancy
            SelBox_surface.set_alpha(40)                # alpha level
            x_tl,y_tl = getCoordinatesOfTopLeftCorner(x_i,y_i,x_m,y_m)
            selection_box = pygame.draw.rect(SelBox_surface, color_green, (0,0,int(math.fabs(x_m-x_i)),int(math.fabs(y_m-y_i))))
            BACKGROUND_SURFACE.blit(SelBox_surface, (x_tl,y_tl))
        except:
            pass
        unitSelection(selection_box, xy_list)

def unitSelection(selection_box, xy_list):
    '''
    To be commented
    old code (must be able to do it something like this instead of ugly shit down below)
    for unit in unit_list:
        if selection_box.colliderect(unit) == 1:
            unit.is_selected = 1
            unit.image = pygame.image.load('images/unit_selected.png').convert()
        elif selection_box.colliderect(unit) == 0:
            unit.is_selected = 0
            unit.image = pygame.image.load('images/unit_unselected.png').convert()
    '''

    for unit in unit_list:
        x = unit.rect.centerx
        y = unit.rect.centery
        isInside = isInsideBox(x,y,xy_list)
        if isInside == 1:
            unit.is_selected = 1
            unit.image = pygame.image.load('images/unit_selected.png').convert()
        elif isInside == 0:
            unit.is_selected = 0
            unit.image = pygame.image.load('images/unit_unselected.png').convert()

def isInsideBox(x,y,xy_list):
    if xy_list[0] < xy_list[2]:
        x_interval = range(xy_list[0] ,xy_list[2]+1)
    elif xy_list[0] > xy_list[2]:
        x_interval = range(xy_list[2] ,xy_list[0]+1)
    if xy_list[1] < xy_list[3]:
        y_interval = range(xy_list[1] ,xy_list[3]+1)
    elif xy_list[1] > xy_list[3]:
        y_interval = range(xy_list[3] ,xy_list[1]+1)

    if x in x_interval and y in y_interval:
        return 1
    else:
        return 0


#=============================INITIALIZATION=====================================
pygame.init()       #Initialize pygame module (required before calling any pygame stuff
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
#==============DEFINE COLORs================================================
color_black = pygame.Color(0,0,0,255)
color_white = pygame.Color(255, 255, 255)
color_red = pygame.Color(255,0,0)
color_green = pygame.Color(0,255,0)
color_blue = pygame.Color(0,0,255)
color_freedom_start_menu = pygame.Color(150,150,150)
inact_color_start_Btn = pygame.Color(200,200,200)
inact_color_quit_Btn = pygame.Color(200,200,200)
act_color_start_Btn = pygame.Color(100,100,100)
act_color_quit_Btn = pygame.Color(100,100,100)

#==============DEFINE DISPLAY SCREEN======================================
BACKGROUND_SURFACE = pygame.display.set_mode((display_pixel_width,display_pixel_height))
pygame.display.set_caption('Freedom')

#set background of the display surface to white
BACKGROUND_SURFACE.fill(color_white)

#initialize bullet list which is update in event handler.
all_sprites_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
unit_list = pygame.sprite.Group()
#Add soldier and put in sprites list
soldier1 = Soldier()
all_sprites_list.add(soldier1)
unit_list.add(soldier1)

#=====================START MENU============================================
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def start_menu():
    '''
    This function is a loop which implements a start menu.
    '''
    pygame.mixer.music.load('sounds/startmenusong2.wav') #Background music
    pygame.mixer.music.play(loops = -1 ,start = 0.0)#-1 : inifinite loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        BackGround = Background('images/gen_troops.png', [0,0])
        BACKGROUND_SURFACE.fill([255, 255, 255])
        BACKGROUND_SURFACE.blit(BackGround.image, BackGround.rect)
        #BACKGROUND_SURFACE.fill(color_blue)

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects('Freedom', largeText, color_freedom_start_menu)
        TextRect.center = ((display_pixel_width/2) , (display_pixel_height/2))
        BACKGROUND_SURFACE.blit(TextSurf, TextRect)
        #Draw and interact with the start and quit buttons:
        pos_start_Btn = ((display_pixel_width/3)-40,(display_pixel_height/1.4),100,50)
        pos_quit_Btn = (2*(display_pixel_width/3)-40,(display_pixel_height/1.4),100,50)

        #createButton(btn_text, pos_tuple, inact_color, act_color):
        mouse_on_start = createButton('Start',pos_start_Btn, act_color_start_Btn, inact_color_start_Btn)
        mouse_on_quit = createButton('Quit', pos_quit_Btn, act_color_quit_Btn, inact_color_quit_Btn)

        if mouse_on_start and pygame.mouse.get_pressed()[0] == 1:
            pygame.mixer.music.fadeout(5000)
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
        BACKGROUND_SURFACE.fill(color_white)# Clear the screen

        #=============Event handler===============
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN \
                and pygame.mouse.get_pressed()[0] == 1:
                    initial_xy = pygame.mouse.get_pos() #used in drawSelectionBox()
                    # which is called below in the game_loop()

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    createBullets()

        #=======SPRITES======================
        all_sprites_list.update() # This is a nice feature to quickly call the update()
        #method for all of the sprites in this list.

        for bullet in bullet_list:
            # Remove the bullet when out of bounds
            if bullet.rect.y < -5 or bullet.rect.x < -5:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        all_sprites_list.draw(BACKGROUND_SURFACE)# Draw all the sprites

        #=======SELECTION BOX================
        try:
            #This will fail when we have not had a MOUSEBUTTONDOWN event.
            drawSelectionBox(initial_xy)
        except:
            pass
        #=========UPDATE DISPLAY AND REFRESH RATE==============
        #Events handled and possibly game state changed: update display accordingly
        pygame.display.flip()# Go ahead and update the screen with what we've drawn.
        fpsClock.tick(FPS)

start_menu()
game_loop()
