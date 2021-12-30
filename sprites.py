import pygame
import random
from pygame import mixer
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
        if key[pygame.K_LEFT]:
            self.image = self.left_image
            dx -= moveSpeed
        if key[pygame.K_RIGHT]:
            self.image = self.right_image
            dx += moveSpeed
        if key[pygame.K_UP]:
            dy -= moveSpeed
        if key[pygame.K_DOWN]:
            dy += moveSpeed
        if key[pygame.K_j]:
            self.score += 1

        # add the delta to the the current location
        # (no collision detection)
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

    def draw_score(self):
        font = pygame.font.SysFont(None, 48)
        img = font.render(f'PLAYER SCORE: {self.score}', True, (0, 0, 0))
        self.game.screen.blit(img, (TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE))
