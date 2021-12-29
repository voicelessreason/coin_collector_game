import pygame, sys
from pygame import mixer
from world import World
from sprites import *
from config import *


class Game:
    # Initialize pygame nuts and bolts
    def __init__(self):
        mixer.init()
        pygame.init()
        pygame.mixer.music.load('sounds/theme.wav')
        pygame.mixer.music.set_volume(.30)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    # Main Game Loop
    def main(self):
        pygame.mixer.music.play()
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False
        pygame.mixer.music.stop()

    # Initialize a new game...construct sprite groups, world and player objects
    def new(self):
        self.playing = True
        self.all_sprites_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.world = World(self, WORLD_DATA)
        self.player = Player(self, TILE_SIZE, TILE_SIZE)


    def events(self):
        # check that we haven't quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites_group.update()

    def draw(self):
        self.screen.fill(WHITE)
        self.world.draw()
        self.all_sprites_group.draw(self.screen)
        self.player.drawScore()
        self.clock.tick(FPS)
        pygame.display.update()

    def game_over(self):
        pass


g = Game()
# g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()


pygame.quit()
sys.exit()
