import pygame
from typing import Optional
from constants import *

class Background(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    pos_x: float

    def __init__(self, group: pygame.sprite.Group, scale_factor: float):
        super().__init__(group)  # the Background instance belong to this group
        bg = pygame.image.load('photos/bg.png').convert()
        bg = pygame.transform.rotozoom(bg, 0, scale_factor)
        self.image = pygame.Surface((bg.get_width() * 2, WINDOW_HEIGHT))
        self.image.blit(bg, (0, 0))
        self.image.blit(bg, (bg.get_width(), 0))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos_x = self.rect.x

    def update(self, dt: float) -> None:
        """The Background Image move to left 100 pixels per second"""
        self.pos_x -= 50 * dt
        if self.rect.centerx <= 0:
            # update self.pos_x!!!
            self.pos_x = 0
        self.rect.x = round(self.pos_x)


class Player(pygame.sprite.Sprite):
    """
    Instance Attributes:
        - velocity: change in distance per second
        - gravity: change in velocity per second. Downward Acceleration. UNCHANGEABLE
    """
    gravity: int
    velocity: float
    def __init__(self, group: pygame.sprite.Group, scale_factor: float):
        super().__init__(group)
        image1 = pygame.image.load('photos/player-1.png').convert_alpha()
        image1 = pygame.transform.rotozoom(image1, 0, scale_factor)
        image2 = pygame.image.load('photos/player-2.png').convert_alpha()
        image2 = pygame.transform.rotozoom(image2, 0, scale_factor)
        # images
        self.frames = [image1, image2]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        # position
        self.rect = self.image.get_rect(center=(PLAYER_CENTER_X, WINDOW_HEIGHT // 2))
        self.rect_pos = list(self.rect.topleft)
        # gravity
        self.gravity = 450
        self.velocity = 0
        # create a mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float) -> None:
        """Update Velocity first, then change images, then rotates the changed image"""
        self.animate_gravity(dt)
        self.animate(dt)
        self.rotate(dt)

    def rotate(self, dt: float) -> None:
        self.image = pygame.transform.rotozoom(self.image, -self.velocity * 0.03, 1)
        self.mask = pygame.mask.from_surface(self.image)

    def animate(self, dt: float) -> None:
        """Change the frame_index by three times per second"""
        self.frame_index += 1 * dt
        if self.frame_index > 1:
            self.frame_index = 0
        self.image = self.frames[round(self.frame_index)]

    def animate_gravity(self, dt: float) -> None:
        """Falls self.gravity pixels per second"""
        self.velocity += self.gravity * dt
        self.rect_pos[1] += self.velocity * dt
        self.rect.y = round(self.rect_pos[1])

    def jump(self, dt: float) -> None:
        """Speed up to -200 pixel per second at this moment"""
        self.velocity = -200

    def get_height(self) -> int:
        return round(self.rect.height)

class Obstacle(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    pos: pygame.Vector2
    speed: int
    direction: str
    counted: bool
    def __init__(self, group: list[pygame.sprite.Group], scale_factor: float, x: int, y: int, direction: str):
        super().__init__(group)
        # image
        self.image = pygame.image.load('photos/pipe.png').convert_alpha()
        self.direction = direction
        if direction == 'top':
            self.image = pygame.transform.rotozoom(self.image, 180, scale_factor)
        else:  # bottom
            self.image = pygame.transform.rotozoom(self.image, 0, scale_factor)
        # position
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 80
        # mask
        self.mask = pygame.mask.from_surface(self.image)
        self.counted = False

    def update(self, dt: float):
        """Pipes move to left by 100 pixels per second"""
        global score
        self.pos.x -= self.speed * dt
        if self.pos.x < -100:
            print('pipes killed')
            self.kill()
        self.rect.x = round(self.pos.x)
        # 每当上面的管道超过了player而且没被计算过，那么计算一次。
        if self.direction == 'top' and not self.counted and self.rect.right < PLAYER_CENTER_X:
            self.counted = True
            score += 1

class Score(pygame.sprite.Sprite):
    def __init__(self):
        global score
        score = 0
        self.score = score
        self.image = FONT.render(f'Score: {self.score}', True, 'Red')
        self.rect = self.image.get_rect(topleft=(0, 0))

    def draw(self, screen: pygame.Surface):
        self.score = score
        self.image = FONT.render(f'Score: {self.score}', True, BLUE)
        # todo：因为local issue mac的不兼容问题，必须放置一个Surface在text底下才可以
        bg = pygame.Surface(self.image.get_size())
        bg.fill('White')
        screen.blit(bg, (0, 0))
        screen.blit(self.image, (0, 0))
