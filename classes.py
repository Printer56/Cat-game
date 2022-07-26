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

        # hitbox
        # self.hitbox = self.walkLeft(self.x, self.y, width, height)
        self.hitbox = self.walkLeft.get_rect(topleft=(self.x, self.y))

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

        # self.hitbox = (self.x, self.y, self.width, self.height)
        self.hitbox = self.walkLeft.get_rect(topleft=(self.x, self.y))
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        print('hit')


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

        self.hitbox = self.image.get_rect(topleft=(self.x, self.y))

    def fall(self, win):
        self.y += self.vel
        win.blit(self.image, (self.x, self.y))

        self.hitbox = self.image.get_rect(topleft=(self.x, self.y))
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

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

        self.hitbox = pygame.Rect(self.x/2, self.y/2, radius * 2, radius * 2)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 0)
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class Powerup(Rock):
    def __init__(self, width) -> None:
        super().__init__(width)

        self.type = random.randint(1, 3)
        self.name = ""

        self.hitbox = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

        match self.type:
            case 1:
                # faster movement
                self.name = "speed"
                self.color = (255, 0, 0)
            case 2:
                # shoot bullets twice as fast
                self.name = "shoot"
                self.color = (0, 255, 0)
            case 3:
                # more money when destroying rock
                self.name = "money"
                self.color = (0, 0, 255)

    def fall(self, win):
        self.y += self.vel
        # line needed for when i get a sprite of the powerups
        # win.blit(self.image, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size_x, self.size_y))

    def activate_powerup(self):
        return self.type