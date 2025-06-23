class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Bullet
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15

        self.bullet_color = (155, 155, 155)
        self.bullet_mag = 10

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
