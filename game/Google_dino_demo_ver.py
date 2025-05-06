import pygame
import random

pygame.init()

screen_width = 1800
screen_height = 800
ground_height = 100
ground_y = screen_height - ground_height
FPS = 30
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Google_dino")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (200, 200, 200)
GRAY = (83, 83, 83)

font = pygame.font.Font(None, 36)



class Dino:
    def __init__(self):
        self.image = pygame.image.load("dino0000.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = pygame.Rect(100, ground_y, 80, 80)
        self.gravity = 0
        self.jump = False

    def update(self):
        self.gravity += 0.8
        self.rect.y += self.gravity
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.jump = False

    def draw(self):
        screen.blit(self.image, self.rect)


class Cactus:
    BASE_SPEED = 10
    speed_increase = 0.005
    def __init__(self):
        self.cactus_width = random.randint(100, 260)
        self.cactus_height = random.randint(120, 190)
        self.rect = pygame.Rect(
            screen_width + self.cactus_width,
            ground_y - self.cactus_height + 15,
            self.cactus_width,
            self.cactus_height,
        )

        self.speed = random.randint(10, 20)
        self.spawn_delay = random.randint(30, 120)
        self.waiting = True
        self.delay_counter = 0

    def update(self):
        if self.waiting:
            self.delay_counter += 1
            if self.delay_counter >= self.spawn_delay:
                self.waiting = False
        else:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.__init__()
        # self.rect.x -= self.speed
        # if self.rect.right < 0:
        #     self.rect.left = screen_width
        #     self.rect.height = self.cactus_height

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)


def background():
    pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, screen_width, screen_height))


def show_game_over():
    text = font.render("Game Over", True, GRAY)
    screen.blit(text, (screen_width // 2, screen_height // 2))


def main():
    dino = Dino()
    cactus = Cactus()
    game_run = True
    game_over = False

    game_run = True
    while game_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not dino.jump and not game_over:
                    dino.gravity = -20
                    dino.jump = True
                # if event.key == pygame.K_s and not dino.jump and not game_over:
                #     dino.rect.bottom = ground_y + 20
                if event.key == pygame.K_r and game_over:
                    main()
                    return
        if not game_over:
            dino.update()
            cactus.update()
            if dino.rect.colliderect(cactus.rect):
                game_over = True
        # Отрисовка
        screen.fill(WHITE)
        background()
        dino.draw()
        cactus.draw()
        if game_over:
            show_game_over()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
