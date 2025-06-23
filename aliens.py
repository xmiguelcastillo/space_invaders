import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, ai_game, image_path, alien_sprite):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.alien_type = alien_sprite

        self.image = pygame.image.load(image_path)
        alien_width = self.settings.screen_width // 25
        alien_height = self.settings.screen_height // 25
        new_size = (alien_width, alien_height)
        self.image = pygame.transform.scale(self.image, new_size)

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        if self.rect.right >= self.settings.screen_width or self.rect.left <= 0:
            return True
        return False
