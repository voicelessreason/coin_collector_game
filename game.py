import sys
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True

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
        self.world = World(self, WORLD_DATA)
        self.player = Player(self, TILE_SIZE, TILE_SIZE)
        self.scoreboard = PlayerScore(self, self.player)
        self.game_timer = GameTimer(self)

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
        self.screen.fill(WHITE)
        self.world.draw()
        self.all_sprites_group.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def game_over(self):
        font = pygame.font.SysFont(None, 60)
        game_over_text = font.render('GAME OVER!', True, BLACK)
        score_text = font.render(f'Score: {self.player.score}', True, BLACK)
        retry_text = font.render('Press Space to Play Again', True, BLACK)
        game_over_location = ((SCREEN_WIDTH // 3) + TILE_SIZE, SCREEN_HEIGHT // 6)
        score_location = ((SCREEN_WIDTH // 4) + (TILE_SIZE * 4), SCREEN_HEIGHT // 4)
        retry_location = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)

        for sprite in self.all_sprites_group:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                self.new()
                self.main()
                self.game_over()

            self.screen.fill(WHITE)
            self.world.draw()
            self.screen.blit(game_over_text, game_over_location)
            self.screen.blit(score_text, score_location)
            self.screen.blit(retry_text, retry_location)
            pygame.display.update()


g = Game()
# g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
