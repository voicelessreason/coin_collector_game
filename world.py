from sprites import *
import random


class World:
    def __init__(self, game, data):
        self.game = game
        self.bg = pygame.image.load('img/space.jpeg')
        self.tileList = []
        treeImg = pygame.transform.scale(pygame.image.load('img/asteroid.png'), (TILE_SIZE, TILE_SIZE))

        row_cnt = 0
        for row in data:
            col_cnt = 0
            for tile in row:
                if tile == 1:
                    img_rect = treeImg.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (treeImg, img_rect)
                    self.tileList.append(tile)
                col_cnt += 1
            row_cnt += 1

    def add_coins(self):
        while len(self.game.coin_group.sprites()) < MAX_COIN_COUNT:
            x = random.randint(1, 18)
            y = random.randint(1, 18)
            Coin(self.game, x * TILE_SIZE, y * TILE_SIZE)
            if pygame.sprite.spritecollide(self.game.player, self.game.coin_group, True):
                self.add_coins()

    def add_enemies(self):
        while len(self.game.enemy_group.sprites()) < ENEMY_COUNT:
            x = random.randint(3, 18)
            y = random.randint(3, 18)
            speed = random.randint(1, 3)
            Enemy(self.game, x * TILE_SIZE,  y * TILE_SIZE, speed)

    def draw(self):
        self.game.screen.blit(self.bg, (0, 0))
        self.add_coins()
        self.add_enemies()
        for tile in self.tileList:
            self.game.screen.blit(tile[0], tile[1])

