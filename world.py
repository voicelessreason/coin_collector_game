from sprites import *
import random


class World:
    def __init__(self, game, data, fullscreen_helper):
        self.game = game
        self.tileList = []
        self.fh = fullscreen_helper
        treeImg = pygame.transform.scale(pygame.image.load('img/asteroid.png'), (self.fh.tile_size, self.fh.tile_size))

        row_cnt = 0
        for row in data:
            col_cnt = 0
            for tile in row:
                if tile == 1:
                    img_rect = treeImg.get_rect()
                    img_rect.x = col_cnt * self.fh.tile_size
                    img_rect.y = row_cnt * self.fh.tile_size
                    tile = (treeImg, img_rect)
                    self.tileList.append(tile)
                col_cnt += 1
            row_cnt += 1

    def add_coins(self):
        while len(self.game.coin_group.sprites()) < MAX_COIN_COUNT:
            x = random.randint(1, 18)
            y = random.randint(1, 18)
            Coin(self.game, x * self.fh.tile_size, y * self.fh.tile_size, self.fh.tile_size)
            if pygame.sprite.spritecollide(self.game.player, self.game.coin_group, True):
                self.add_coins()

    def add_enemies(self):
        while len(self.game.enemy_group.sprites()) < ENEMY_COUNT:
            x = random.randint(3, 18)
            y = random.randint(3, 18)
            speed = random.randint(1, 3)
            Enemy(self.game, x * self.fh.tile_size,  y * self.fh.tile_size, speed, self.fh.tile_size)

    def draw(self):
        self.game.screen.blit(self.game.bg, (0, 0))
        self.add_coins()
        self.add_enemies()
        for tile in self.tileList:
            self.game.screen.blit(tile[0], tile[1])

