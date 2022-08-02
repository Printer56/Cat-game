import pygame
import random
from classes import Player, Powerup, Rock, Projectile

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

score = 0

# how many miliseconds you have in between shots
shoot_time = 1000
canShoot = True

run = True

# loading background
bg = pygame.image.load("assets/images/bg.png")
bg = pygame.transform.scale(bg, (width, height))

def redrawScreen():
    win.blit(bg, (0, 0))
    cat.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    for rock in rocks:
        rock.fall(win)

    pygame.display.update()

def generate_rocks(n: int) -> None:
    # generates n number of rocks on the screen
    chance = random.randint(1, 4)
    powerup = True if chance == 4 else False

    for num in range(n):
        rock = Rock(width)
        if powerup:
            rock = Powerup(width)
            powerup = False
        rocks.append(rock)

def shoot_bullet():
    direction = -1 if cat.left else 1
    x = cat.x
    if direction == 1:
        x = x + cat.width
    y = cat.y + cat.width/2
    bullet = Projectile(x, y, 5, pygame.Color(0, 255, 0), direction)

    bullets.append(bullet)

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
            if bullet.hitbox.colliderect(rock.hitbox):
                rocks.pop(rocks.index(rock))
                bullets.pop(bullets.index(bullet))
                if isinstance(rock, Powerup): break
                score += 1
                print(score)
                break

    for rock in rocks:
        # cat hit rocks
        if cat.hitbox.colliderect(rock.hitbox):
            if isinstance(rock, Powerup):
                power = rock.activate_powerup()

                match power:
                    case 1:
                        cat.speed *= 2
                    case 2:
                        shoot_time /= 2
                    case 3:
                        pass
            else:
                cat.hit()
            rocks.pop(rocks.index(rock))
        elif rock.y >= height - rock.size_y:
            rocks.pop(rocks.index(rock))

    # getting key presses
    keys = pygame.key.get_pressed()

    # move left
    if keys[pygame.K_LEFT] and cat.x > 0:
        cat.left, cat.right = True, False
        cat.x -= cat.speed

        if cat.x < 0:
            cat.x = 0
    # move right
    if keys[pygame.K_RIGHT] and cat.x < width - cat.width:
        cat.left, cat.right = False, True
        cat.x += cat.speed

        if cat.x > width - cat.width:
            cat.x = width - cat.width

    # jump function
    if not cat.isJump:
        if keys[pygame.K_UP]:
            cat.isJump = True
    else:
        cat.jump()

    # shoot projectile, only once per second
    if keys[pygame.K_SPACE] and canShoot:
        shoot_bullet()
        canShoot = False
        start2 = now

    if not canShoot and now - start2 > shoot_time: canShoot = True

    # spawn rocks every 2 seconds
    now = pygame.time.get_ticks()
    if now - start1 > 2000:
        generate_rocks(2)
        start1 = now

    redrawScreen()