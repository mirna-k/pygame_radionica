import pygame, sys, time, random
from settings import *
from sprites import Background, Bird, Obsticle

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.active = True
        
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.pipe_sprites = pygame.sprite.Group()

        # sprites
        Background(self.all_sprites)
        self.bird = Bird(self.all_sprites)

        # timer
        self.obsticle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obsticle_timer, 1500)

        # font
        self.font = pygame.font.Font('graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.passing_pipe = False

        # restart menu
        self.restart_surface = pygame.image.load('graphics/ui/restart.png').convert_alpha()
        self.restart_rect = self.restart_surface.get_rect(center = (WIDTH/2, HEIGHT/2))


    def display_score(self):
        score_surface = self.font.render(str(self.score), True, 'black')
        score_rect = score_surface.get_rect(midtop = (WIDTH/2, HEIGHT/30))
        self.screen.blit(score_surface, score_rect)
    

    def collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.pipe_sprites, False, pygame.sprite.collide_mask)\
            or self.bird.rect.bottom <= -100 or self.bird.rect.bottom >= HEIGHT + 100:
            for sprite in self.pipe_sprites.sprites():
                sprite.kill()
            self.bird.kill()
            self.active = False


    def run(self):
        last_time = time.time()

        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            if len(self.pipe_sprites) > 0:
                if self.bird.rect.right < self.pipe_sprites.sprites()[0].rect.right and self.passing_pipe == False:
                    self.passing_pipe = True
                    
                if self.passing_pipe and self.bird.rect.left > self.pipe_sprites.sprites()[0].rect.right:
                    self.score += 1
                    self.passing_pipe = False

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.obsticle_timer and self.active:
                    pipe_height = random.randint(200, 400)
                    Obsticle('down', pipe_height, [self.all_sprites, self.pipe_sprites])
                    Obsticle('up', pipe_height, [self.all_sprites, self.pipe_sprites])

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if self.active:
                    self.bird.jump()
                else:
                    self.bird = Bird(self.all_sprites)
                    self.active = True
                    self.score = 0

            if self.active:
                self.all_sprites.update(dt)
                self.all_sprites.draw(self.screen)
                self.collisions()
            else:
                self.screen.blit(self.restart_surface, self.restart_rect)
            self.display_score()

            # game logic
            pygame.display.update()
        
            self.clock.tick(FRAMERATE)