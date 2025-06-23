import pygame
from settings import Settings


class Ship(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load("./images/ship.png")
        new_size = (50, 50)

        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False
        self.moving_left = False

        self.ship_speed = 4.5

        self.settings = Settings()

    def movement(self):
        if self.moving_right:
            self.rect.x += self.ship_speed
        if self.moving_left:
            self.rect.x -= self.ship_speed

    def boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width

    def blitload(self):
        self.screen.blit(self.image, self.rect)
