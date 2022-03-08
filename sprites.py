import pygame, random
from config import *


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y, fullscreen_helper):
        self.fh = fullscreen_helper
        self.image = pygame.transform.scale(pygame.image.load('img/coin.png'), (self.fh.tile_size // 2, self.fh.tile_size // 2))
        self.game = game
        self.groups = [self.game.all_sprites_group, self.game.coin_group]
        self.rect = self.image.get_rect()
        self.rect.x = x + self.fh.play_area_offset['x']
        self.rect.y = y + self.fh.play_area_offset['y']
        pygame.sprite.Sprite.__init__(self, self.groups)


class Player(pygame.sprite.Sprite):
    def __init__(self, game, fullscreen_helper):
        self.fh = fullscreen_helper
        self.tile_dimensions = (self.fh.tile_size, self.fh.tile_size)
        self.right_image = pygame.transform.scale(pygame.image.load('img/player.png'), self.tile_dimensions)
        self.left_image = pygame.transform.flip(self.right_image, 180, 0)
        self.image = self.right_image
        self.coinFx = pygame.mixer.Sound('sounds/coin.wav')
        self.coinFx.set_volume(GLOBAL_VOLUME)
        self.deathFx = pygame.mixer.Sound('sounds/game_over.wav')
        self.deathFx.set_volume(100)
        self.game = game
        self.groups = self.game.all_sprites_group
        self.rect = self.image.get_rect()
        self.rect.x = self.tile_dimensions[0] + self.fh.play_area_offset['x']
        self.rect.y = self.tile_dimensions[1] + self.fh.play_area_offset['y']
        self.score = 0
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        moveSpeed = 10
        dx = 0
        dy = 0

        # handle key input
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.image = self.left_image
            dx -= moveSpeed
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.image = self.right_image
            dx += moveSpeed
        if key[pygame.K_UP] or key[pygame.K_w]:
            dy -= moveSpeed
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            dy += moveSpeed

        # add the delta to the the current location
        self.rect.x += dx
        self.rect.y += dy

        # Bind the player within the world
        buffer = self.fh.tile_size
        offset_bottom = self.fh.play_area_offset['y'] - buffer
        offset_top = self.fh.play_area_offset['y'] + buffer
        offset_right = self.fh.play_area_offset['x'] - buffer
        offset_left = self.fh.play_area_offset['x'] + buffer

        if self.rect.bottom > self.fh.actual_play_area_size[1] + offset_bottom:
            self.rect.bottom = self.fh.actual_play_area_size[1] + offset_bottom
        if self.rect.top < offset_top:
            self.rect.top = offset_top
        if self.rect.right > self.fh.actual_play_area_size[0] + offset_right:
            self.rect.right = self.fh.actual_play_area_size[0] + offset_right
        if self.rect.left < offset_left:
            self.rect.left = offset_left

        # check if we've hit a coin
        if pygame.sprite.spritecollide(self, self.game.coin_group, True):
            self.score += 1
            self.coinFx.play()

        if pygame.sprite.spritecollide(self, self.game.enemy_group, False):
            self.deathFx.play()
            self.game.playing = False


class PlayerScore(pygame.sprite.Sprite):
    def __init__(self, game, player, fullscreen_helper):
        self.player = player
        self.game = game
        self.fh = fullscreen_helper
        self.font = pygame.font.SysFont(None, self.fh.actual_subheader_font_size)
        self.image = self.font.render(f'SCORE: 0', True, TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = self.fh.tile_size
        self.rect.y = self.fh.actual_play_area_size[1] - self.fh.tile_size
        self.groups = self.game.all_sprites_group
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.image = self.font.render(f'SCORE: {self.player.score}', True, TEXT_COLOR)


class GameTimer(pygame.sprite.Sprite):
    def __init__(self, game, fullscreen_helper):
        self.game = game
        self.fh = fullscreen_helper
        self.start_ticks = pygame.time.get_ticks()
        self.groups = self.game.all_sprites_group
        self.font = pygame.font.SysFont(None, self.fh.actual_header_font_size)
        self.image = self.font.render(f'{START_TIME}', True, TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = self.fh.desktop_resolution[0] - self.image.get_width() - self.fh.tile_size
        self.rect.y = self.fh.tile_size
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        time_remaining = START_TIME - seconds

        if time_remaining <= 0:
            self.game.playing = False

        self.image = self.font.render(f'{time_remaining}', True, TEXT_COLOR)
        self.game.clock.tick(FPS)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, speed, fullscreen_helper):
        self.onScreen = True
        self.game = game
        self.moveSpeed = speed
        self.fh = fullscreen_helper
        self.explosionFx = pygame.mixer.Sound('sounds/explosion.wav')
        self.explosionFx.set_volume(GLOBAL_VOLUME)
        self.groups = [self.game.all_sprites_group, self.game.enemy_group]
        self.right_image = pygame.transform.scale(pygame.image.load('img/enemy.png'), (self.fh.tile_size, self.fh.tile_size))
        self.left_image = pygame.transform.flip(self.right_image, 180, 0)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.x = x + self.fh.play_area_offset['x']
        self.rect.y = y + self.fh.play_area_offset['y']
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        if self.onScreen == False:
            return

        dx = 0
        dy = 0
        xdiff = self.rect.x - self.game.player.rect.x + random.randint(-10, 10)
        ydiff = self.rect.y - self.game.player.rect.y + random.randint(-10, 10)

        if xdiff > 0:
            dx -= self.moveSpeed
        if xdiff < 0:
            dx += self.moveSpeed
        if ydiff < 0:
            dy += self.moveSpeed
        if ydiff > 0:
            dy -= self.moveSpeed

        self.rect.x += dx
        self.rect.y += dy

        collisions = pygame.sprite.spritecollide(self, self.game.enemy_group, False)
        if len(collisions) > 2:
            self.explosionFx.play()
            Explosion(self.game, self.rect.x, self.rect.y)
            self.onScreen = False
            self.rect.x = -1000
            self.rect.y = -1000
            self.game.enemy_group.remove(self)
            self.game.player.score += 5


class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = [self.game.all_sprites_group, self.game.explosion_group]
        self.images = [pygame.image.load('img/explosion1.png'),
                       pygame.image.load('img/explosion2.png'),
                       pygame.image.load('img/explosion3.png'),
                       pygame.image.load('img/explosion4.png'),
                       pygame.image.load('img/explosion5.png')]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
        self.index = 0
        self.explosion_speed = 2
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.counter += 1
        if self.counter >= self.explosion_speed:
            self.index += 1
            self.counter = 0

        if self.index < len(self.images):
            self.image = self.images[self.index]
        else:
            self.kill()

    def draw(self):
        self.game.screen.blit(self.image)
