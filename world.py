from sprites import *


class World:
    def __init__(self, game, data):
        self.game = game
        self.tileList = []
        grassImg = pygame.transform.scale(pygame.image.load('img/grass.png'), (TILE_SIZE, TILE_SIZE))
        treeImg = pygame.transform.scale(pygame.image.load('img/tree.png'), (TILE_SIZE, TILE_SIZE))

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
                if tile == 2:
                    img_rect = grassImg.get_rect()
                    img_rect.x = col_cnt * TILE_SIZE
                    img_rect.y = row_cnt * TILE_SIZE
                    tile = (grassImg, img_rect)
                    self.tileList.append(tile)
                col_cnt += 1
            row_cnt += 1

    def add_coins(self):
        if len(self.game.coin_group.sprites()) < self.game.max_coin_count:
            Coin(self.game, random.randint(1, 18) * TILE_SIZE, random.randint(1, 18) * TILE_SIZE)


    def draw(self):
        self.add_coins()
        for tile in self.tileList:
            self.game.screen.blit(tile[0], tile[1])
