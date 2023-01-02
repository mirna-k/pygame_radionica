import pygame, random

pygame.init()

WIDTH = 480
HEIGHT = 800
FRAMERATE = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

ligth_blue = (173, 216, 230)

clock = pygame.time.Clock()

# PLAYER
player_image = pygame.image.load('graphics/bird/bird1.png')
player = player_image.get_rect(center = (WIDTH/4, HEIGHT/2))

# OBSTACLES
pasage_gap = 200
pasage_height = random.randint(200, 400)

down_pipe_image = pygame.image.load('graphics/obstacles/pipe.png')
down_pipe = down_pipe_image.get_rect(topleft = (WIDTH, pasage_height + pasage_gap/2))
up_pipe_image = pygame.transform.flip(down_pipe_image, False, True)
up_pipe = up_pipe_image.get_rect(bottomleft = (WIDTH, pasage_height - pasage_gap/2))


def window():
    SCREEN.fill(ligth_blue)
    SCREEN.blit(player_image, (player.x, player.y))
    SCREEN.blit(down_pipe_image, (down_pipe.x, down_pipe.y))
    SCREEN.blit(up_pipe_image, (up_pipe.x, up_pipe.y))
    pygame.display.update()


def player_movement(pressed_key):
    gravity = 5
    position = pygame.math.Vector2(player.topleft)
    position.y += gravity
    player.y = position.y

    if pressed_key[pygame.K_SPACE]:
        player.y -= 15


def pipe_movement():
    speed = 3
    down_pipe_pos = pygame.math.Vector2(down_pipe.topleft)
    down_pipe_pos.x -= speed
    down_pipe.x = down_pipe_pos.x

    up_pipe_pos = pygame.math.Vector2(up_pipe.topleft)
    up_pipe_pos.x -= speed
    up_pipe.x = up_pipe_pos.x


def main():
    run = True
    while run == True:
        clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pressed_key = pygame.key.get_pressed()

        window()
        player_movement(pressed_key)
        pipe_movement()

    pygame.quit()

if __name__ == "__main__":
    main()