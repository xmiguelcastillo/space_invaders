import pygame


class AlienLaser(pygame.sprite.Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255, 0, 0) 

        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = x
        self.rect.bottom = y
        self.y = float(self.rect.y)

    def update(self):
        self.y += 2
        self.rect.y = self.y

    def draw_laser(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
