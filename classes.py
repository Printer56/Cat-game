import pygame
import random

char = pygame.image.load("assets/cat_stand_right.gif")

class Player:
    # This is the main player
    def __init__(self, x, y, width=50, height=50) -> None:
        # starting coordinates and size
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # initialize images
        self.walkLeft = pygame.image.load("assets/cat_stand_left.gif")
        self.walkLeft = pygame.transform.scale(self.walkLeft, (width, height))

        self.walkRight = pygame.image.load("assets/cat_stand_right.gif")
        self.walkRight = pygame.transform.scale(self.walkRight, (width, height))

        # starting speed
        self.speed = 5

        # left or right facing, start facing right
        self.left = False
        self.right = True

        # jumping variables
        self.isJump = False
        self.jumpCount = 8

    def draw(self, win):
        if self.right:
            win.blit(self.walkRight, (self.x, self.y))
            self.left, self.right = False,  True
        elif self.left:
            win.blit(self.walkLeft, (self.x, self.y))
            self.left, self.right = True, False
        else:
            direction = self.walkLeft if self.left else self.walkRight
            win.blit(direction, (self.x, self.y))


class Rock:
    # Rock is a projectile that falls from random x values from the sky

    # Make little bits of fire branching off from rock?
    
    def __init__(self, width) -> None:
        self.x = random.randint(0, width - 50)
        self.y = 0

        self.size_x = 30
        self.size_y = 30

        self.vel = random.randint(5, 15)

        self.image = pygame.image.load("assets/rock.png")
        self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

    def fall(self, win):
        self.y += self.vel
        win.blit(self.image, (self.x, self.y))

class Projectile:
    # Projectile is an object (like a bullet) that shoots out of the cat to either push other players into rocks or destroy rocks

    def __init__(self, x, y, radius, color, facing) -> None:
        # coordinates of bullet
        self.x = x
        self.y = y
        # radius of bullet
        self.radius = radius
        self.color = color
        # which direction the bullet is going (left (-1) or right (1))
        self.facing = facing

        self.vel = 10 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 0)