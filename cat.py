import pygame
import random
from classes import Player, Rock, Projectile

# initialize screen and pygame
pygame.init()
size = width, height = 500, 500
center = width/2, height/2
win = pygame.display.set_mode(size)
pygame.display.set_caption("Cat!")

# set game variables
cat = Player(x=center[0], y=center[1] + 190)

rocks = []
bullets = []

start1 = pygame.time.get_ticks()
start2 = pygame.time.get_ticks()

run = True

# loading background
bg = pygame.image.load("assets/bg.png")
bg = pygame.transform.scale(bg, (width, height))

def redrawScreen():
    win.blit(bg, (0, 0))
    cat.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    for rock in rocks:
        rock.fall(win)

    pygame.display.update()

while run:
    # display background
    win.blit(bg, (0, 0))

    # controls speed of game
    pygame.time.delay(50)

    # makes sure user can quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

    for bullet in bullets:
        if bullet.x < width and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    for rock in rocks:
        if rock.y >= height - rock.size_y:
            rocks.pop(rocks.index(rock))

    # getting key presses
    keys = pygame.key.get_pressed()

    # move left
    if keys[pygame.K_LEFT] and cat.x > 0:
        cat.left, cat.right = True, False
        cat.x -= cat.speed
    # move right
    if keys[pygame.K_RIGHT] and cat.x < width - cat.width:
        cat.left, cat.right = False, True
        cat.x += cat.speed

    # jump function
    if not cat.isJump:
        if keys[pygame.K_UP]:
            cat.isJump = True

    else:
        if cat.jumpCount >= -8:
            neg = 1
            if cat.jumpCount < 0:
                neg = -1
            y = -((cat.jumpCount ** 2) / 2 * neg)
            cat.jumpCount -= 1
            cat.y += y
        else:
            cat.isJump = False
            cat.jumpCount = 8

    # shoot projectile, only once per second
    if keys[pygame.K_SPACE] and now - start2 > 1000:
        start2 = now
        direction = -1 if cat.left else 1
        x = cat.x
        if direction == 1:
            x = x + cat.width
        y = cat.y + cat.width/2
        bullet = Projectile(x, y, 5, pygame.Color(0, 255, 0), direction)

        bullets.append(bullet)

    # spawn rocks every 2 seconds
    now = pygame.time.get_ticks()
    if now - start1 > 2000:
        vel1 = random.randint(10, 20)
        vel2 = random.randint(10, 20)
        start1 = now
        rock1 = Rock(width)
        rock2 = Rock(width)
        rocks.append(rock1)
        rocks.append(rock2)

    redrawScreen()