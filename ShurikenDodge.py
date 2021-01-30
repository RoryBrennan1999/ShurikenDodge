import os
import random
import sys

import pygame

os.environ['SDL_VIDEODRIVER'] = 'directx'

pygame.init()  # Initialize package

# Screen Dimensions
ScreenWidth = 500
ScreenHeight = 480

win = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.DOUBLEBUF) # Create window

pygame.display.set_caption("Shuriken Dodge")  # Label window

clock = pygame.time.Clock()  # Create system clock

# Score variable
score = 0

# Load in images, music and sound effects
walkRight = [pygame.image.load('assets/R0.png').convert_alpha(), pygame.image.load('assets/R1.png').convert_alpha(),
             pygame.image.load('assets/R2.png').convert_alpha(),
             pygame.image.load('assets/R3.png').convert_alpha(), pygame.image.load('assets/R4.png').convert_alpha(),
             pygame.image.load('assets/R5.png').convert_alpha()]
walkLeft = [pygame.image.load('assets/L0.png').convert_alpha(), pygame.image.load('assets/L1.png').convert_alpha(),
            pygame.image.load('assets/L2.png').convert_alpha(),
            pygame.image.load('assets/L3.png').convert_alpha(), pygame.image.load('assets/L4.png').convert_alpha(),
            pygame.image.load('assets/L5.png').convert_alpha()]
shuriken = [pygame.image.load('assets/shuriken1.png').convert_alpha(), pygame.image.load('assets/shuriken2.png').convert_alpha(),
            pygame.image.load('assets/shuriken3.png').convert_alpha(),
            pygame.image.load('assets/shuriken4.png').convert_alpha()]
jumpUpR = pygame.image.load('assets/jump_0R.png').convert_alpha()
jumpUpL = pygame.image.load('assets/jump_0L.png').convert_alpha()
jumpUp = pygame.image.load('assets/jump_0.png').convert_alpha()
dead_R = pygame.image.load('assets/death_R.png').convert_alpha()
dead_L = pygame.image.load('assets/death_L.png').convert_alpha()
platForm = pygame.image.load('assets/platform.png').convert_alpha()
bg = pygame.image.load('assets/bg.jpeg').convert_alpha()
mm = pygame.image.load('assets/mm.jpeg').convert_alpha()
tips = pygame.image.load('assets/tips.png').convert_alpha()
char = pygame.image.load('assets/idle_0.png').convert_alpha()
jumpSound = pygame.mixer.Sound('assets/jump.wav')
hitSound = pygame.mixer.Sound('assets/hit.wav')
knockSound = pygame.mixer.Sound('assets/knock.wav')
music = pygame.mixer.music.load('assets/music.wav')
pygame.mixer.music.set_volume(0.3)  # Set volume
pygame.mixer.music.play(-1)  # Continuously play music


# Create classes and objects
class Player(object):
    def __init__(self, x, y, width, height, ):
        self.x = x
        self.y = y
        self.width = width
        self.vel = 6
        self.height = height
        self.isDead = False
        self.isJump = False
        self.isFalling = False
        self.fallCount = 0
        self.jumpCount = 9
        self.onPlatform = False
        self.onTop = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.hitbox = (self.x + 20, self.y + 17, 28, 33)

    def draw(self, win):
        if self.walkCount + 1 >= 30:
            self.walkCount = 0

        if self.left and not self.isJump:
            win.blit(walkLeft[self.walkCount // 6], (self.x, self.y))
            self.walkCount += 1
        elif self.right and not self.isJump:
            win.blit(walkRight[self.walkCount // 6], (self.x, self.y))
            self.walkCount += 1
        elif self.isJump and self.right:
            win.blit(jumpUpR, (self.x, self.y))
        elif self.isJump and self.left:
            win.blit(jumpUpL, (self.x, self.y))
        elif self.isJump and (not self.left or not self.right):
            win.blit(jumpUp, (self.x, self.y))
        else:
            win.blit(char, (self.x, self.y))
        if self.isDead and self.right:
            win.blit(dead_R, (self.x, self.y))
        elif self.isDead and self.left:
            win.blit(dead_L, (self.x, self.y))
        elif self.isDead and not self.left and not self.right:
            win.blit(dead_R, (self.x, self.y))
        if self.left:
            self.hitbox = (self.x + 30, self.y + 17, 28, 32)  # Move hitbox (hitbox was slightly off while moving left
        else:
            self.hitbox = (self.x + 20, self.y + 17, 28, 32)  # Move hitbox
        # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):  # Player Hit System
        self.isJump = False
        self.isFalling = False
        self.draw(win)
        self.jumpCount = 9
        self.walkCount = 0
        self.x = 40
        self.y = 400
        fontHit = pygame.font.SysFont('papyrus', 50, bold=True)
        text = fontHit.render('Shameful Display!', 1, (255, 255, 255))
        win.blit(text, ((ScreenWidth // 2) - (text.get_width() // 2), 215))
        pygame.display.update()
        i = 0
        while i < 250:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def move(self):
        if keys[pygame.K_a] and self.x > self.vel:
            self.x -= self.vel
            self.left = True
            self.right = False
        elif keys[pygame.K_d] and self.x < ScreenWidth - self.width - self.vel:
            self.x += self.vel
            self.left = False
            self.right = True
        else:
            self.right = False
            self.left = False
            self.walkCount = 0


class Projectile(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.isPastPlayer = False
        self.moveCount = 0
        self.hitbox = (self.x + 17, self.y + 17, self.width, self.height)

    def move(self):
        self.x -= self.vel  # Shurikens moves from left to right

    def draw(self, win):
        if self.moveCount + 1 >= 8:
            self.moveCount = 0

        if not self.isPastPlayer:
            win.blit(shuriken[self.moveCount // 2], (self.x, self.y))
            self.moveCount += 1

        self.hitbox = (self.x + 22, self.y + 17, self.width, self.height)  # Move hitbox
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self, object, object2, object3):
        # Check if projectiles hit ninja
        if self.hitbox[1] < object.hitbox[1] + object.hitbox[3] and self.hitbox[
            1] + self.height > object.hitbox[1]:  # Checks x coords
            if self.hitbox[0] + self.width > object.hitbox[0] and self.hitbox[0] < \
                    object.hitbox[0] + object.hitbox[2]:  # Checks y coords
                hitSound.play()
                object.onTop = False
                object.isDead = True
                self.resetPosition()
                object2.resetPosition()
                object3.resetPosition()
                object.hit()

        if object2.hitbox[1] < object.hitbox[1] + object.hitbox[3] and object2.hitbox[
            1] + object2.height > object.hitbox[1]:  # Checks x coords
            if object2.hitbox[0] + object2.width > object.hitbox[0] and object2.hitbox[0] < \
                    object.hitbox[0] + object.hitbox[2]:  # Checks y coords
                hitSound.play()
                object.onTop = False
                object.isDead = True
                self.resetPosition()
                object2.resetPosition()
                object3.resetPosition()
                object.hit()

        if object3.hitbox[1] < object.hitbox[1] + object.hitbox[3] and object3.hitbox[
            1] + object3.height > object.hitbox[1]:  # Checks x coords
            if object3.hitbox[0] + object3.width > object.hitbox[0] and object3.hitbox[0] < \
                    object.hitbox[0] + object.hitbox[2]:  # Checks y coords
                hitSound.play()
                object.onTop = False
                object.isDead = True
                self.resetPosition()
                object2.resetPosition()
                object3.resetPosition()
                object.hit()

    def resetPosition(self):
        self.y = random.randrange(70, 400)
        self.x = random.randrange(480, 650)
        pass

    def speed(self):
        # Check difficulty and increase speed
        if 6 >= score >= 3:
            self.vel = random.randrange(12, 14)
        elif 9 >= score > 6:
            self.vel = random.randrange(13, 15)
        elif 12 >= score > 9:
            self.vel = random.randrange(14, 16)
        elif 15 >= score > 12:
            self.vel = random.randrange(15, 17)
        elif score > 15:
            self.vel = random.randrange(16, 22)
        else:
            self.vel = random.randrange(11, 13)


class Platform(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(platForm, (self.x, self.y))
        pygame.draw.rect(win, (0, 0, 0), self.hitbox, 2)

class Background(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hitbox = (self.x, self.y, ScreenWidth, ScreenHeight)

    def draw(self, win):
        win.blit(bg, (self.x, self.y))

class Text(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 20, 20)

    def draw(self, win):
        font = pygame.font.SysFont('javanesetext', 20, True)  # Score box
        text_score = font.render('Score: ' + str(score) + '                               ' + 'High Score: ' + str(hi_score), 1, (255, 255, 255))
        win.blit(text_score, (self.x, self.y))

# Create objects and relevant variables
ninja = Player(40, 400, 80, 58)  # Create ninja object
flying_star_1 = Projectile(520, random.randrange(90, 250), 30, 45, 8)  # Create shuriken objects
flying_star_2 = Projectile(640, random.randrange(290, 390), 30, 45, 8)
flying_star_3 = Projectile(820, random.randrange(90, 390), 30, 45, 8)
plat1 = Platform(0, 310, 500, 30)  # Create platforms
plat2 = Platform(0, 175, 500, 30)
background = Background()
text_obj = Text(25, 0)
hi_score = 0
run = True
introStart = True

# Draw sprites, background and texts
def redrawWindow():
    background.draw(win)
    text_obj.draw(win)
    plat1.draw(win)
    plat2.draw(win)
    flying_star_1.draw(win)
    flying_star_2.draw(win)
    flying_star_3.draw(win)
    ninja.draw(win)
    pygame.display.flip()


# Create intro screen with tips/instructions
def intro():
    win.blit(mm, (0, 0))
    font1 = pygame.font.SysFont('javanesetext', 60)
    title = font1.render('Shuriken Dodge', 1, (0, 0, 0))
    win.blit(title, ((ScreenWidth // 2) - (title.get_width() // 2), 205))
    ninja.draw(win)
    font2 = pygame.font.SysFont('javanesetext', 25)
    text = font2.render('Loading.... ', 1, (0, 0, 0))
    win.blit(text, (370, 350))
    pygame.display.update()
    i = 0
    while i < 300:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    i = 0
    win.blit(tips, (0, 0))  # Show tips/instructions
    ninja.draw(win)
    win.blit(text, (370, 350))
    pygame.display.update()
    while i < 800:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Main Loop
while run:

    clock.tick(30)  # 30 FPS
    ninja.isDead = False  # Revive ninja

    # Intro Screen
    while introStart:
        intro()
        introStart = False

    redrawWindow()

    for event in pygame.event.get():  # Check for events such as key press, mouse press etc
        if event.type == pygame.QUIT:
            run = False

    if hi_score < score:  # Update High Score
        hi_score = score

    keys = pygame.key.get_pressed()  # Move sprite/ boundaries

    ninja.move()
    flying_star_1.move()
    flying_star_2.move()
    flying_star_3.move()
    flying_star_1.hit(ninja, flying_star_2, flying_star_3)

    # Platform mechanics
    if (plat1.hitbox[1] - 20) < ninja.hitbox[1] + ninja.hitbox[3] < plat1.hitbox[1] and ninja.hitbox[1] > plat2.hitbox[
        1] + plat2.hitbox[3]:
        ninja.x = plat1.x + (ninja.x - plat1.x)
        ninja.y = plat1.y - ninja.height + 10
        ninja.isJump = False
        ninja.onPlatform = True
        ninja.fallCount = 0
        ninja.jumpCount = 9

    if plat2.hitbox[1] - 20 < ninja.hitbox[1] + ninja.hitbox[3] < plat2.hitbox[1] and ninja.hitbox[1] < plat1.hitbox[
        1] + plat1.hitbox[3] and not ninja.isFalling:
        ninja.x = plat2.x + (ninja.x - plat2.x)
        ninja.y = plat2.y - ninja.height + 10
        ninja.isJump = False
        ninja.onPlatform = True
        ninja.onTop = True
        ninja.fallCount = 0
        ninja.jumpCount = 9

    if flying_star_1.x < -70:
        flying_star_1.x = random.randrange(500, 550)
        flying_star_1.y = random.randrange(90, 380)
        score += 1

    if flying_star_2.x < -70:
        flying_star_2.x = random.randrange(500, 550)
        flying_star_2.y = random.randrange(90, 380)

    if flying_star_3.x < -70:
        flying_star_3.x = random.randrange(500, 550)
        flying_star_3.y = random.randrange(90, 380)

    if ninja.isDead:
        score = 0

    flying_star_1.speed()  # Change speed based on score
    flying_star_2.speed()
    flying_star_3.speed()

    # Ctrl-Q to quit
    if keys[pygame.K_q] & keys[pygame.KMOD_CTRL]:
        pygame.quit()

    if keys[pygame.K_s]:
        ninja.onPlatform = False
        ninja.isFalling = True
        ninja.onTop = False
    if ninja.isFalling and not ninja.isJump:  # Falling System
        ninja.y -= (ninja.fallCount ** 2) // 2 * -1
        ninja.fallCount -= 1
        if ninja.fallCount <= -14:
            ninja.fallCount = 0
        if plat1.y + 20 > ninja.y > plat1.y and not (keys[pygame.K_s]):
            ninja.y = plat1.y - ninja.height + 10
            ninja.isFalling = False
            ninja.fallCount = 0
            ninja.onPlatform = True
        if ninja.y > 380:
            ninja.y = 400
            ninja.isFalling = False
            ninja.fallCount = 0
    else:
        ninja.isFalling = False
        ninja.fallCount = 0

    if not ninja.isJump:  # Jumping System
        if keys[pygame.K_SPACE]:
            if not ninja.onTop and not (keys[pygame.K_s]) and not ninja.isFalling:
                jumpSound.play()
                ninja.isJump = True
                ninja.right = False
                ninja.left = False
                ninja.walkCount = 0
    else:
        if ninja.jumpCount >= -18 and not (keys[pygame.K_s]):
            neg = 1
            ninja.isFalling = False
            if ninja.jumpCount < 0:  # This moves us downwards towards end of jump
                ninja.isFalling = True
                neg = -1
            ninja.y -= (ninja.jumpCount ** 2) // 2 * neg
            ninja.jumpCount -= 1
            if ninja.y > 380:
                ninja.y = 400
                ninja.isJump = False
                ninja.jumpCount = 9
        elif ninja.jumpCount >= -27 and keys[pygame.K_s]:
            neg = 1
            if ninja.jumpCount < 0:  # This moves us downwards towards end of jump
                ninja.isFalling = True
                neg = -1
            ninja.y -= (ninja.jumpCount ** 2) // 2 * neg
            ninja.jumpCount -= 1
            if ninja.y > 380:
                ninja.y = 400
                ninja.isJump = False
                ninja.jumpCount = 9
        else:
            ninja.isFalling = False
            ninja.isJump = False
            ninja.jumpCount = 9

    # Prevent jumping on top platform
    if ninja.onTop and keys[pygame.K_SPACE] or (keys[pygame.K_s] and keys[pygame.K_SPACE]):
        ninja.isJump = False
        # knockSound.play()

pygame.quit()
