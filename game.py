import sys
from pygame import mixer
from fullscreen_helper import FullscreenHelper
from world import World
from sprites import *
from config import *


class Game:
    # Initialize pygame nuts and bolts
    def __init__(self):
        mixer.init()
        pygame.init()
        pygame.mixer.music.load('sounds/theme.wav')
        pygame.mixer.music.set_volume(GLOBAL_VOLUME)

        desktop_size = pygame.display.get_desktop_sizes()[0]
        self.fh = FullscreenHelper(desktop_size)
        
        self.bg = pygame.image.load('img/space.jpeg')
        # Scale the background image to match the desktop resolution
        self.bg = pygame.transform.scale(self.bg, self.fh.desktop_resolution)
        self.screen = pygame.display.set_mode(self.fh.desktop_resolution)
        self.running = True

    def intro_screen(self):
        self.font = pygame.font.SysFont(None, 60)
        self.screen.blit(self.bg, (0, 0))
        begin_text = self.font.render('Press Space to Begin', True, TEXT_COLOR)
        begin_rect = ((self.fh.actual_play_area_size[0] // 4) + self.fh.tile_size, self.fh.actual_play_area_size[1] // 3)

        self.screen.blit(begin_text, begin_rect)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                return

            pygame.display.update()

    # Main Game Loop
    def main(self):
        pygame.mixer.music.play()
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.stop()

    # Initialize a new game...construct sprite groups, world and player objects
    def new(self):
        self.clock = pygame.time.Clock()
        self.playing = True
        self.all_sprites_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.world = World(self, WORLD_DATA, self.fh)
        self.player = Player(self, self.fh)
        self.scoreboard = PlayerScore(self, self.player, self.fh)
        self.game_timer = GameTimer(self, self.fh)

    # Process any global events
    def events(self):
        # check that we haven't quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    # Update all sprites
    def update(self):
        self.all_sprites_group.update()

    # Draw all sprites
    def draw(self):
        self.world.draw()
        self.all_sprites_group.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def game_over(self):
        header_font = pygame.font.SysFont(None, self.fh.actual_header_font_size)
        subheader_font = pygame.font.SysFont(None, self.fh.actual_subheader_font_size)
        game_over_text = header_font.render('GAME OVER!', True, TEXT_COLOR)
        score_text = subheader_font.render(f'Score: {self.player.score}', True, TEXT_COLOR)
        retry_text = subheader_font.render('Press Space to Play Again', True, TEXT_COLOR)
        quit_text = subheader_font.render('Press Escape to Quit', True, TEXT_COLOR)

        text_x = (self.fh.actual_play_area_size[0] // 3) + self.fh.tile_size
        game_over_location = (text_x, self.fh.actual_play_area_size[1] // 2.5)
        score_location = (text_x, self.fh.actual_play_area_size[1] // 2)
        retry_location = (text_x, self.fh.actual_play_area_size[1] // 1.9)
        quit_location = (text_x, self.fh.actual_play_area_size[1] // 1.8)

        for sprite in self.all_sprites_group:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                for sprite in self.all_sprites_group:
                    sprite.kill()

                self.screen.blit(self.bg, (0, 0))
                self.new()
                self.main()
                self.game_over()
            if key[pygame.K_ESCAPE]:
                self.running = False

            self.screen.blit(self.bg, (0, 0))
            self.world.draw()
            self.screen.blit(game_over_text, game_over_location)
            self.screen.blit(score_text, score_location)
            self.screen.blit(retry_text, retry_location)
            self.screen.blit(quit_text, quit_location)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
