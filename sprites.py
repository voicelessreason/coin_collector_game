import pygame, copy
from config import *


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.image = pygame.transform.scale(pygame.image.load('img/coin.png'), (TILE_SIZE // 2, TILE_SIZE // 2))
        self.game = game
        self.groups = [self.game.all_sprites_group, self.game.coin_group]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pygame.sprite.Sprite.__init__(self, self.groups)


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.right_image = pygame.transform.scale(pygame.image.load('img/player.png'), (TILE_SIZE, TILE_SIZE))
        self.left_image = pygame.transform.flip(self.right_image, 180, 0)
        self.image = self.right_image
        self.coinFx = pygame.mixer.Sound('sounds/coin.wav')
        self.coinFx.set_volume(GLOBAL_VOLUME)
        self.deathFx = pygame.mixer.Sound('sounds/game_over.wav')
        self.deathFx.set_volume(100)
        self.game = game
        self.groups = self.game.all_sprites_group
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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
        buffer = TILE_SIZE
        if self.rect.bottom > SCREEN_HEIGHT - buffer:
            self.rect.bottom = SCREEN_HEIGHT - buffer
        if self.rect.top < TILE_SIZE:
            self.rect.top = TILE_SIZE
        if self.rect.right > SCREEN_WIDTH - buffer:
            self.rect.right = SCREEN_WIDTH - buffer
        if self.rect.left < buffer:
            self.rect.left = buffer

        # check if we've hit a coin
        if pygame.sprite.spritecollide(self, self.game.coin_group, True):
            self.score += 1
            self.coinFx.play()

        if pygame.sprite.spritecollide(self, self.game.enemy_group, False):
            self.deathFx.play()
            self.game.playing = False


class PlayerScore(pygame.sprite.Sprite):
    def __init__(self, game, player):
        self.player = player
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.image = self.font.render(f'PLAYER SCORE: 0', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = TILE_SIZE
        self.rect.y = SCREEN_HEIGHT - TILE_SIZE
        self.groups = self.game.all_sprites_group
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.image = self.font.render(f'PLAYER SCORE: {self.player.score}', True, (0, 0, 0))


class GameTimer(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.start_ticks = pygame.time.get_ticks()
        self.groups = self.game.all_sprites_group
        self.font = pygame.font.SysFont(None, 60)
        self.image = self.font.render(f'{START_TIME}', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2) - TILE_SIZE
        self.rect.y = 0
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        time_remaining = START_TIME - seconds

        if time_remaining <= 0:
            self.game.playing = False

        self.image = self.font.render(f'{time_remaining}', True, (0, 0, 0))
        self.game.clock.tick(FPS)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        self.onScreen = True
        self.game = game
        self.moveSpeed = speed
        self.explosionFx = pygame.mixer.Sound('sounds/explosion.wav')
        self.explosionFx.set_volume(GLOBAL_VOLUME)
        self.groups = [self.game.all_sprites_group, self.game.enemy_group]
        self.right_image = pygame.transform.scale(pygame.image.load('img/enemy.png'), (TILE_SIZE, TILE_SIZE))
        self.left_image = pygame.transform.flip(self.right_image, 180, 0)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        if self.onScreen == False:
            return

        dx = 0
        dy = 0
        xdiff = self.rect.x - self.game.player.rect.x
        ydiff = self.rect.y - self.game.player.rect.y

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
            self.onScreen = False
            self.rect.x = -1000
            self.rect.y = -1000
            self.game.enemy_group.remove(self)
            self.game.player.score += 5
