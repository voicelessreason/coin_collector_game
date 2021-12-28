import sys, pygame
from pygame import mixer

mixer.init
pygame.init()

screenWidth = 1000
screenHeight = 1000
screenTitle = 'Hell Yeah Brother'

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption(screenTitle)
clock = pygame.time.Clock()

# load images and set variables
skyImg = pygame.image.load('img/sky.png')
dirtImg = pygame.image.load('img/dirt.png')
platformImg = pygame.image.load('img/platform.png')
grassImg = pygame.image.load('img/grass.png')
treeImg = pygame.image.load('img/tree.png')

coinFx = pygame.mixer.Sound('sounds/coin.wav')

gameState = 'menu'
tileSize = 50
lineCount = int(screenWidth / tileSize)


def drawGrid():
    for line in range(0, lineCount):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tileSize), (screenWidth, line * tileSize))
        pygame.draw.line(screen, (255, 255, 255), (line * tileSize, 0), (line * tileSize, screenHeight))


def drawScore(score):
    font = pygame.font.SysFont(None, 48)
    img = font.render(f'PLAYER SCORE: {score}', True, (0, 0, 0))
    screen.blit(img, (tileSize, screenHeight - tileSize))


def drawWorld():
    drawGrid()


class World:
    def __init__(self, data):
        self.tileList = []

        row_cnt = 0
        for row in data:
            col_cnt = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(treeImg, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * tileSize
                    img_rect.y = row_cnt * tileSize
                    tile = (img, img_rect)
                    self.tileList.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grassImg, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = col_cnt * tileSize
                    img_rect.y = row_cnt * tileSize
                    tile = (img, img_rect)
                    self.tileList.append(tile)
                if tile == 3:
                    coin_group.add(Coin(col_cnt * tileSize, row_cnt * tileSize))
                col_cnt += 1
            row_cnt += 1

    def draw(self):
        for tile in self.tileList:
            screen.blit(tile[0], tile[1])


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tileSize // 2, tileSize // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)


worldData = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Player:
    def __init__(self, x, y):
        img = pygame.image.load('img/player.png')
        self.image = pygame.transform.scale(img, (tileSize, tileSize))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score = 0

    def update(self):
        moveSpeed = 5
        dx = 0
        dy = 0

        # handle key input
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= moveSpeed
        if key[pygame.K_RIGHT]:
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
        buffer = tileSize
        if self.rect.bottom > screenHeight - buffer:
            self.rect.bottom = screenHeight - buffer
        if self.rect.top < tileSize:
            self.rect.top = tileSize
        if self.rect.right > screenWidth - buffer:
            self.rect.right = screenWidth - buffer
        if self.rect.left < buffer:
            self.rect.left = buffer

        # check if we've hit a coin

        if pygame.sprite.spritecollide(self, coin_group, True):
            self.score += 1
            coinFx.play()

        screen.blit(self.image, self.rect)


coin_group = pygame.sprite.Group()
world = World(worldData)
player = Player(tileSize, tileSize)

run = True
while run:

    if gameState == 'menu':
        screen.blit(skyImg, (0, 0))
        gameState = 'main'
    if gameState == 'main':
        # draw the world
        screen.fill((255, 255, 255))
        world.draw()
        player.update()
        coin_group.draw(screen)
        drawScore(player.score)
    if gameState == 'over':
        print('over')

    # check that we haven't quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update the display and advance time
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
