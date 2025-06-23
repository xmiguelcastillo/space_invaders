import pygame


class Shields(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("./images/shields.png")
        shield_width = self.settings.screen_width // 10
        shield_height = self.settings.screen_height // 22
        new_size = (shield_width, shield_height)
        self.image = pygame.transform.scale(self.image, new_size)

        self.rect = self.image.get_rect()
        self.health = 3

    def hit(self):
        self.health -= 1

        darken_alpha = int((1 - (self.health / 5)) * 255)

        dark_surface = pygame.Surface(self.image.get_size()).convert_alpha()
        dark_surface.fill((0, 0, 0, darken_alpha))

        self.image.blit(dark_surface, (0, 0))

        if self.health <= 0:
            self.kill()
