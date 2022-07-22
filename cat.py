import pygame
from classes import Player, Rock

# initialize screen and pygame
pygame.init()
size = width, height = 500, 500
center = width/2, height/2
win = pygame.display.set_mode(size)
pygame.display.set_caption("Cat!")

# set game variables
cat = Player(x=center[0], y=center[1] + 190)

rock = Rock(width)

run = True

# loading background
bg = pygame.image.load("assets/bg.png")
bg = pygame.transform.scale(bg, (width, height))

def redrawScreen():
    win.blit(bg, (0, 0))
    cat.draw(win)

    if rock.y < height:
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

    # getting key presses
    keys = pygame.key.get_pressed()

    # move left
    if keys[pygame.K_a]:
        cat.left, cat.right = True, False
        cat.x -= cat.speed[0]
    # move right
    if keys[pygame.K_d]:
        cat.left, cat.right = False, True
        cat.x += cat.speed[0]

    # jump function
    if not cat.isJump:
        if keys[pygame.K_SPACE]:
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

    redrawScreen()