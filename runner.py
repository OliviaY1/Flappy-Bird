import time, sys, random
from constants import *
from sprites import Background, Player, Obstacle, Score

class Game():
    screen: pygame.Surface
    clock: pygame.time.Clock
    obstacle_timer: int
    all_sprites: pygame.sprite.Group
    collision_sprites: pygame.sprite.Group
    player: Player
    scale_factor: float
    pipe_height: int
    active: bool

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Birds')
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        bg_height = pygame.image.load('photos/bg.png').convert().get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height
        Background(self.all_sprites, self.scale_factor)

        # used for generate_obstacle
        pipe_image = pygame.image.load('photos/pipe.png').convert_alpha()
        pipe_image = pygame.transform.rotozoom(pipe_image, 0, self.scale_factor / 13)
        self.pipe_height = pipe_image.get_height()

        self.start_game()

    def start_game(self):
        """Create self.player. Create obstacle_timer and set timer. Create self.score. self.active True"""
        self.player = Player(self.all_sprites, self.scale_factor / 25)
        # set timer for obstacles
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, OBSTACLE_CREATE_TIME)
        self.score = Score()
        # game status
        self.active = True

    def run(self) -> None:
        prev_time = time.time()
        while True:
            dt = time.time() - prev_time
            prev_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.active:
                    if event.type == pygame.KEYDOWN:
                        self.player.jump(dt)
                    if event.type == self.obstacle_timer:
                        print('New pipe created')
                        self.generate_obstacle()
                else:
                    if event.type == pygame.KEYDOWN:
                        # start the game
                        self.start_game()

            # GAME LOGIC
            self.screen.fill('Blue')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            self.display_score()

            # check collision here
            if self.active:
                self.collision()
            else:
                self.display_result()
            pygame.display.update()
            self.clock.tick(50)

    def collision(self):
        if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask):
            self.active = False
            self.player.kill()
            self.all_sprites.remove(self.collision_sprites)
            self.collision_sprites.empty()

    def display_result(self):
        # self.screen.fill('White')
        text = FONT.render(f' Your score is:{self.score.score}! \n Press Any key to Restart', True, BLUE)
        # todo: add a rectangle below the score due to mac bugs
        bg = pygame.Surface(text.get_size())
        bg.fill('White')
        self.screen.blit(bg, text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))
        self.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))


    def generate_obstacle(self):
        """Create two obstacles, wiz interval > self.player.get_height()"""
        x = random.randint(WINDOW_WIDTH + 20, WINDOW_WIDTH + 40)
        top_x, bottom_x = x, x
        top_y = random.randint(-400, -10)
        interval = random.randint(self.player.get_height() + 30, self.player.get_height() + 200)
        bottom_y = top_y + self.pipe_height + interval
        Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor / 13, top_x, top_y, 'top')
        Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor / 13, bottom_x, bottom_y, 'bottom')

    def display_score(self):
        self.score.draw(self.screen)
