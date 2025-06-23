import pygame
import sys
import os
from settings import Settings
from ship import Ship
from bullet import Bullet
from aliens import Alien
from shields import Shields
import random
from lasers import AlienLaser

os.environ["SDL_VIDEO_WINDOW_POS"] = "1"


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_height, self.settings.screen_width)
        )
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()

        pygame.mixer.init()
        pygame.mixer.music.load("./music.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        self.points = 0

        self.alien_lasers = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        self._create_fleet()
        self._create_shields()

    def run_game(self):
        while True:
            self.clock.tick(60)
            self._check_events()

            self.ship.movement()
            self.ship.boundaries()

            self.bullets.update()
            self._check_fleet_edges()
            self.aliens.update()

            self.font = pygame.font.Font("./retro.otf", 30)
            self.game_text()

            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            self._update_screen()

    def _create_shields(self):
        shield_spacing = self.settings.screen_width // 5
        for i in range(4):
            shield = Shields(self)
            shield.rect.x = shield_spacing * (i + 1) - shield.rect.width // 2
            shield.rect.y = self.settings.screen_height - 150
            self.shields.add(shield)

    def _create_fleet(self):
        temp_alien = Alien(self, "./images/squid.png", "squid")
        alien_width, alien_height = temp_alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        for row_number in range(5):
            for alien_number in range(number_aliens_x):
                if row_number == 0:
                    img = "./images/squid.png"
                    alien_sprite = "squid"
                elif row_number in (1, 2):
                    img = "./images/octupus.png"
                    alien_sprite = "octupus"
                elif row_number in (3, 4):
                    img = "./images/crab.png"
                    alien_sprite = "crab"
                else:
                    img = "./images/squid.png"
                    alien_sprite = "squid"

                self._create_alien(alien_number, row_number, img, alien_sprite)

    def _create_alien(self, alien_number, row_number, img, alien_sprite):
        alien = Alien(self, img, alien_sprite)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number + 80
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def bullet_sound(self):
        bullet_sound = pygame.mixer.Sound("./shoot.wav")
        bullet_sound.play()

    def death_sound(self):
        death_sound = pygame.mixer.Sound("./explosion.wav")
        death_sound.play()

    def kill_sound(self):
        kill_sound = pygame.mixer.Sound("./kill.wav")
        kill_sound.set_volume(0.4)
        kill_sound.play()

    def death_sound(self):
        death_sound = pygame.mixer.Sound("./explosion.wav")
        death_sound.play()

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):

        if len(self.bullets) < self.settings.bullet_mag:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullet_sound()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.read_scores()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._event_key_down(event)
            if event.type == pygame.KEYUP:
                self._event_key_up(event)

    def _event_key_down(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.read_scores()
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _event_key_up(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def game_text(self):
        f = open("./scores.txt")
        hi_score = f.readline().strip()

        # Score

        self.text_score_title = self.font.render("SCORE<1>", True, (56, 243, 255))
        self.text_score = self.font.render(f"000{self.points}", True, (255, 255, 255))

        # Score Rect
        self.text_rect1 = self.text_score_title.get_rect(topleft=(50, 10))
        self.text_rect2 = self.text_score.get_rect(topleft=(90, 50))

        # Hi-Score
        self.text_hi_score_title = self.font.render("HI-SCORE", True, (94, 91, 255))
        self.text_hi_score = self.font.render(f"{hi_score}", True, (255, 255, 255))

        # Hi-Score Rect
        self.text_rect3 = self.text_hi_score_title.get_rect(topleft=(300, 10))
        self.text_rect4 = self.text_hi_score.get_rect(topleft=(370, 50))

        # Score 2
        self.text_score_title2 = self.font.render("SCORE<2>", True, (255, 224, 156))
        self.text_score2 = self.font.render("00000", True, (255, 255, 255))

        # Hi-Score Rect
        self.text_rect5 = self.text_score_title2.get_rect(topleft=(570, 10))
        self.text_rect6 = self.text_score2.get_rect(topleft=(610, 50))

    def read_scores(self):
        with open("./scores.txt", "r") as f:
            line = f.readline().strip()
            if line:
                self.hi_score = int(line)
            else:
                self.hi_score = 0
        if self.points > self.hi_score:
            with open("./scores.txt", "w") as f:
                f.write(str(self.points))

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitload()
        self.ship.blitload()
        # SCORE
        self.screen.blit(self.text_score_title, self.text_rect1)
        self.screen.blit(self.text_score, self.text_rect2)

        # HI_SCORE
        self.screen.blit(self.text_hi_score_title, self.text_rect3)
        self.screen.blit(self.text_hi_score, self.text_rect4)

        for alien in self.aliens.sprites():
            if random.randint(1, 200) == 1:
                laser = AlienLaser(self, alien.rect.centerx, alien.rect.bottom)
                if len(self.alien_lasers) < 3:
                    self.alien_lasers.add(laser)

        self.alien_lasers.update()
        for laser in self.alien_lasers:
            laser.draw_laser()
            if laser.rect.top > self.settings.screen_height:
                self.alien_lasers.remove(laser)

        # SCORE 2
        self.screen.blit(self.text_score_title2, self.text_rect5)
        self.screen.blit(self.text_score2, self.text_rect6)
        self.shields.draw(self.screen)

        death = pygame.sprite.groupcollide(
            pygame.sprite.GroupSingle(self.ship),
            self.aliens,
            True,
            True,
        )
        death2 = pygame.sprite.groupcollide(
            pygame.sprite.GroupSingle(self.ship),
            self.alien_lasers,
            True,
            True,
        )
        if death:
            self.death_sound()
            self.read_scores()

            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()
        if death2:
            self.death_sound()
            self.read_scores()

            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()
        hits = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if hits:
            self.kill_sound()

        for bullet, aliens_hit in hits.items():
            for alien in aliens_hit:
                if alien.alien_type == "crab":
                    self.points += 20
                if alien.alien_type == "octupus":
                    self.points += 10
                if alien.alien_type == "squid":
                    self.points += 30
                print(f"got a {alien.alien_type}")

        self.aliens.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        hits2 = pygame.sprite.groupcollide(self.shields, self.bullets, False, True)
        for shield, bullets in hits2.items():
            for bullet in bullets:
                shield.hit()

        hits_shield = pygame.sprite.groupcollide(
            self.shields, self.alien_lasers, False, True
        )

        for shield, bullets in hits_shield.items():
            for bullet in bullets:
                shield.hit()
        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()

