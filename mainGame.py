#HC Import modules and setup the basic files needed
import pygame
import sys
import time
from datetime import datetime

pygame.init()

#HC Initialize game screen size
win = pygame.display.set_mode((1280, 720))

#HC Game name
pygame.display.set_caption("Protect Gardener")

#HC Animations for player - while walking
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load(
    'R5.png'), pygame.image.load('R6.png'), pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load(
    'L5.png'), pygame.image.load('L6.png'), pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png')]

#HC Load backgrounds and musics
bg = pygame.image.load('bg.png')
bulletSound = pygame.mixer.Sound("bullet.mp3")
hitSound = pygame.mixer.Sound("hit.wav")
music = pygame.mixer.music.load("round2music.mp3")
letter = pygame.image.load("letter.png")
help_text = pygame.image.load("help_text.png")
phase_text = pygame.image.load("phaseLeft.png")
font = pygame.font.Font("consolaz.ttf", 30)
clearImage = pygame.image.load('clearImage.png')

#HL Timing for game
clock = pygame.time.Clock()

#HC Settings for music
pygame.mixer.init()
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

#HC Class that organized player's data

class player(object):
    #HC Initializing variables required for player
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 7.5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    #HC Animating player's moves

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


#HC Class for bullets
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


#HC and HL Class for enemy
class enemy(object):
    #HC change enemy's picture
    walkRight = [pygame.image.load('E1.png'), pygame.image.load('E2.png'), pygame.image.load('E3.png'), pygame.image.load('E4.png'), pygame.image.load('E5.png'), pygame.image.load(
        'E6.png'), pygame.image.load('E1.png'), pygame.image.load('E2.png'), pygame.image.load('E3.png'), pygame.image.load('E4.png'), pygame.image.load('E5.png'), pygame.image.load('E6.png')]
    walkLeft = [pygame.image.load('E1.png'), pygame.image.load('E2.png'), pygame.image.load('E3.png'), pygame.image.load('E4.png'), pygame.image.load('E5.png'), pygame.image.load(
        'E6.png'), pygame.image.load('E1.png'), pygame.image.load('E2.png'), pygame.image.load('E3.png'), pygame.image.load('E4.png'), pygame.image.load('E5.png'), pygame.image.load('E6.png')]

    #HC Enemy's default setting

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 6
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.maxhealth = 15
        self.health = 15
        self.visible = True
        self.deathcount = 0
        self.phaseLeft = 4

    #HC What enemy does in certain conditions
    def draw(self, win):
        self.move()
        for flower in enemies[:]:
            #HC While visible (not dead)
            if self.visible == True:
                if self.walkCount + 1 >= 33:
                    self.walkCount = 0
                if self.vel > 0:
                    win.blit(
                        self.walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                else:
                    win.blit(
                        self.walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                self.hitbox = (self.x + 17, self.y + 2, 31, 57)
                pygame.draw.rect(
                    win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, (5*self.maxhealth), 10))  #HC HEALTH Bars
                pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, ((
                    5*self.maxhealth)) - (5 * (self.maxhealth - self.health)), 10))  #HC Health bars


    #HC Enemy's movement
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    #HC If enemy got hit
    def hit(self):
        hitSound.play()
        if self.health > 2:
            self.health -= 2
        else:
            self.visible = False
            self.deathcount += 1
            pygame.time.delay(1000)
            if self.deathcount == 0:
                self.phaseLeft = 4
            elif self.deathcount == 1:
                self.health = 20
                self.maxhealth = 20
                self.y = 450
                self.vel = 8
                self.visible = True
                self.phaseLeft = 3
            elif self.deathcount == 2:
                self.health = 25
                self.maxhealth = 25
                self.y = 400
                self.vel = 10
                self.visible = True
                self.phaseLeft = 2
            elif self.deathcount == 3:
                self.health = 30
                self.maxhealth = 30
                self.y = 450
                self.vel = 13
                self.visible = True
                self.phaseLeft = 1
            else:
                self.visible = False
                self.phaseLeft = 0
                pygame.time.delay(5000)
                


#HC define a function for collision detection
def crash():
    global deathCountPlayer
    global crashCheck
#HC check conditions for collision
    if ((man.y > goblin.y and man.y < (goblin.y + 30)) or ((man.y + 30) > goblin.y and (man.y + 30) < (goblin.y + 30))):
        if ((man.x > goblin.x and man.x < (goblin.x + 30)) or ((man.x + 30) > goblin.x and (man.x + 30) < (goblin.x + 30))):
            man.x = 820
            man.y = 300
            deathCountPlayer = deathCountPlayer + 1
            pygame.time.delay(300)
            crashCheck = True
        else:
            crashCheck = False
    else:
        crashCheck = False



#HC and HL Update game's window
def redrawGameWindow():
    displayDeath = font.render("Death Count : {}".format(deathCountPlayer), True, (255,0,0))
    displayPhase = font.render("{}".format(goblin.phaseLeft), True, (255,0,0))
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.draw(win)
    win.blit(help_text, (0, 0))
    win.blit(phase_text, (850, 0))
    win.blit(text_time, (600, 0))
    win.blit(displayDeath, (850, 50))
    win.blit(displayPhase, (1090, 18))
    for bullet in bullets:
        bullet.draw(win)
    if keys[pygame.K_h]:
        win.blit(letter, (260, 0))
    if goblin.phaseLeft == 0:
        white = (255,255,255)
        win.fill(white)
        win.blit(clearImage, (0,0))
        
    pygame.display.update()



#HC and HL mainloop for game
man = player(400, 410, 64, 64)
goblin = enemy(320, 550, 64, 64, 820)
shootLoop = 0
bullets = []
run = True
enemies = []
enemies.append(goblin)
crashCheck = False
deathCountPlayer = 0

#HL and HC 
start_time = datetime.now()
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))

        if bullet.x < 1000 and bullet.x > 300:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

#HL checking time for game
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())
    text_time = font.render("time : {}".format(delta_time), True, (0,0,0))

    keys = pygame.key.get_pressed()
#HC when attacking
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2),
                           round(man.y + man.height//2), 6, (0, 0, 0), facing))

        shootLoop = 1
#HC moving with keys pressed
    if keys[pygame.K_LEFT] and man.x > man.vel and man.x > 310:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    #HC game boundary
    elif keys[pygame.K_RIGHT] and man.x < 950 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    elif keys[pygame.K_UP] and man.y > man.vel and man.y > 280:
        man.y -= man.vel
        man.right = False
        man.left = False
        man.standing = True
    elif keys[pygame.K_DOWN] and man.y < 645 - man.height - man.vel:
        man.y += man.vel
        man.right = False
        man.left = False
        man.standing = True
    else:
        man.standing = True
        man.walkCount = 0

    if crashCheck == True:
        crashCheck = False  

    crash()
    redrawGameWindow()



pygame.quit()
