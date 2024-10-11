from typing import Any
import pygame
from pygame.locals import *
from pygame.sprite import Group
import random
pygame.mixer.init()

pygame.init()

screen_width = 826
screen_height = 552

clock = pygame.time.Clock()
fps = 60

#loading images
bg = pygame.image.load('images/background.jpg')
ground_img = pygame.image.load('images/ground2.jpg')
img = pygame.image.load('images/537-5377529_restart-button-png-images-colorfulness-clipart-removebg-preview.png')

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Get Offended')

font = pygame.font.SysFont('Bauhus 93', 63)
white = (0,0,0)

collision_sound = pygame.mixer.Sound('sound/Allahu Akbar - QuickSounds.com (online-audio-converter.com).wav')

#game variables
ground_scroll = 0
scroll_speed = 4
start = False
game_over = False
tower_gap = 150
tower_frequency = 2000 #milliseconds
last_twinTowers = pygame.time.get_ticks() - tower_frequency
score = 0
mission_failed = False

def restart():
    tower_group.empty()
    plane.rect.x = 100
    plane.rect.y = int(screen_height/2)
    score = 0
    return score
def score_counter(text, font, text_color, x, y):
    image = font.render(text, True, text_color)
    screen.blit(image, (x,y))


class Plane(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/plane.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0
        self.clicked = False
        self.fall_flip = 0

    def update(self):

        if run == False:
            #gravity
            if start == True:
                self.velocity += 0.5
                if self.velocity > 5:
                    self.velocity = 5
                if self.rect.bottom < 504:
                    self.rect.y += self.velocity
        
        if game_over == False:

            # if self.rect.top > 50:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.rotation_angle = -10
                self.velocity = -10
                self.image = pygame.transform.rotate(self.image, self.velocity * -1)

            if pygame.mouse.get_pressed()[0] == 0 :
                self.clicked = False
                self.image = pygame.image.load('images/plane.png')
                self.image = pygame.transform.rotate(self.image, self.velocity * 2)

        elif game_over == True and self.fall_flip == 0:
            self.image = pygame.transform.rotate(self.image, -90)
            self.fall_flip = 1

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, topBottom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/tower (1).png')
        self.rect = self.image.get_rect()
        if topBottom == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y-int(tower_gap/2)]
        if topBottom == -1:
            self.rect.topleft = [x,y+int(tower_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed

        if self.rect.right < 0:
            self.kill()

class Restart_button():
    def __init__(self, x, y, image):
        self.image= image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):

        act = False
        #mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                act = True

            screen.blit(self.image, (self.rect.x, self.rect.y))

        return act
    
plane_group = pygame.sprite.Group()
plane = Plane(100,int(screen_height/2))
plane_group.add(plane)

tower_group = pygame.sprite.Group()

button = Restart_button(int((screen_width/2)-150), int((screen_height/2)-50),img)

run = False

while run != True:

    #clock to stop the program from executing as soon as possible
    clock.tick(fps)

    #background
    screen.blit(bg, (0,0))

    #plane
    plane_group.draw(screen)
    plane_group.update()

    #draw the towers (this is made so up top so they may be behind the ground and not fuk up the rest of game mechanism)
    tower_group.draw(screen)

    #score check
    if len(tower_group)>0:
        if ((plane_group.sprites()[0].rect.left)>(tower_group.sprites()[0].rect.left)) and ((plane_group.sprites()[0].rect.right)>(tower_group.sprites()[0].rect.right)) and mission_failed == False:
            mission_failed = True
        if mission_failed == True:
            if ((plane_group.sprites()[0].rect.left)>(tower_group.sprites()[0].rect.right)):
                score += 1
                mission_failed = False

    score_counter(str(score),font,white,int(screen_width/2),20)
    
    #draw the ground
    screen.blit(ground_img, (ground_scroll,464))

    if plane.rect.bottom > 495:
        game_over = True    
        start = False

    #collision
    if pygame.sprite.groupcollide(plane_group,tower_group,False,False) or plane.rect.top < 0:
        game_over = True
        collision_sound.play()

    #ground scrolling
    if game_over == False and start == True:

        #generating towers
        current_time = pygame.time.get_ticks()
        if current_time - last_twinTowers > tower_frequency:

            tower_rgap = random.randint(-40,40)

            bottom_tower = Tower(screen_width,int((screen_height/2)-15+tower_rgap),-1)
            top_tower = Tower(screen_width,int((screen_height/2)+10+tower_rgap),1)
            tower_group.add(top_tower)
            tower_group.add(bottom_tower)
            last_twinTowers = current_time

        ground_scroll -= scroll_speed
        if abs(ground_scroll)>35:
            ground_scroll = 0

        tower_group.update()

    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = restart()

    #quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = True
        if event.type == pygame.MOUSEBUTTONDOWN and start == False and game_over == False:
            start = True

    #to update otherwise only a black screen will be shown
    pygame.display.update()
    
pygame.quit()