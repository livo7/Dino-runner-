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
        self.img_size = (100, 100)
        self.jump_image = pygame.transform.scale(
            pygame.image.load("dinoJump0000.png").convert_alpha(), self.img_size
        )
        self.run_images = [
            pygame.transform.scale(
                pygame.image.load("dinorun0000.png").convert_alpha(), self.img_size
            ),
            pygame.transform.scale(
                pygame.image.load("dinorun0001.png").convert_alpha(), self.img_size
            ),
        ]
        self.dead_image = pygame.transform.scale(
            pygame.image.load("dinoDead0000.png").convert_alpha(), self.img_size
        )
        self.rect = pygame.Rect(100, ground_y, 80, 80)
        self.gravity = 0
        self.jump = False
        self.dead = False
        self.animation_count = 0
        self.animation_speed = 0.15

    def update(self):
        if not self.jump and not self.dead:
            self.animation_count += self.animation_speed
            if self.animation_count >= len(self.run_images):
                self.animation_count = 0
            self.current_image = self.run_images[int(self.animation_count)]
        elif self.jump and not self.dead:
            self.current_image = self.jump_image
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.jump = False

    def draw_die(self):
        self.dead = True
        self.current_image = self.dead_image

    def draw(self):
        screen.blit(self.current_image, self.rect)


class Cactus:
    def __init__(self):
        self.cactus_tipe = random.randint(1, 3)
        self.setup_cactus()
        self.speed = 15
        self.spawn_delay = random.randint(5, 20)
        self.waiting = True
        self.delay_counter = 0

    def setup_cactus(self):
        if self.cactus_tipe == 1:
            self.cactus_width = 60
            self.cactus_height = 120
            self.image = pygame.image.load("cactusBig0000.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.cactus_width, self.cactus_height))
            self.rect = self.image.get_rect(bottomleft=(screen_width, ground_y + 15))

        elif self.cactus_tipe == 2:
            self.cactus_width = 40
            self.cactus_height = 80
            self.image = pygame.image.load("cactusSmall0000.png").convert_alpha()
            self.rect = self.image.get_rect(bottomleft=(screen_width, ground_y + 15))

        elif self.cactus_tipe == 3:
            self.cactus_width = 120
            self.cactus_height = 80
            self.image = pygame.image.load("cactusSmallMany0000.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.cactus_width, self.cactus_height))
            self.rect = self.image.get_rect(bottomleft=(screen_width, ground_y + 15))

    def update(self):
        if self.waiting:
            self.delay_counter += 1
            if self.delay_counter >= self.spawn_delay:
                self.waiting = False
        else:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.__init__()

    def draw(self):
        screen.blit(self.image, self.rect)


class Berd:
    def __init__(self):
        self.berd_tipe = random.randint(1, 3)
        self.setup_berd()
        self.speed = 15
        self.spawn_delay = random.randint(5, 20)
        self.waiting = True
        self.delay_counter = 0
        self.animation_count = 0
        self.animation_speed = 0.15

    def setup_berd(self):
        if self.berd_tipe == 1:
            self.cactus_width = 90
            self.cactus_height = 80
            self.fly_images = [
                pygame.image.load("berd.png").convert_alpha(),
                pygame.image.load("berd2.png").convert_alpha(),
            ]
            self.rect = pygame.Rect(screen_width, ground_y - 75, 90, 80)
        elif self.berd_tipe == 2:
            self.cactus_width = 90
            self.cactus_height = 80
            self.fly_images = [
                pygame.image.load("berd.png").convert_alpha(),
                pygame.image.load("berd2.png").convert_alpha(),
            ]
            self.rect = pygame.Rect(screen_width, ground_y - 125, 90, 80)
        elif self.berd_tipe == 3:
            self.cactus_width = 90
            self.cactus_height = 80
            self.fly_images = [
                pygame.image.load("berd.png").convert_alpha(),
                pygame.image.load("berd2.png").convert_alpha(),
            ]
            self.rect = pygame.Rect(screen_width, ground_y - 175, 90, 80)

    def update(self):
        if self.waiting:
            self.delay_counter += 1
            if self.delay_counter >= self.spawn_delay:
                self.waiting = False
        else:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.__init__()
        self.animation_count += self.animation_speed
        if self.animation_count >= len(self.fly_images):
            self.animation_count = 0
        self.current_image = self.fly_images[int(self.animation_count)]

    def draw(self):
        screen.blit(self.current_image, self.rect)


def background():
    pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, screen_width, screen_height))


def show_game_over():
    text = font.render("Game Over", True, GRAY)
    screen.blit(text, (screen_width // 2, screen_height // 2))


def main():
    dino = Dino()
    cactus = Cactus()
    berd = Berd()
    game_run = True
    game_over = False

    while game_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not dino.jump and not game_over:
                    dino.gravity = -20
                    dino.jump = True
                if event.key == pygame.K_r and game_over:
                    main()
                    return
        if not game_over:
            if random.random() <= 0.7:
                berd.update()
                flag = "b"
            else:
                cactus.update()
                flag = "c"
            dino.update()
            if flag == "b":
                if dino.rect.colliderect(berd.rect):
                    game_over = True
            if flag == "с":
                if dino.rect.colliderect(cactus.rect):
                    game_over = True
        screen.fill(WHITE)
        background()
        dino.draw()
        if flag == "c":
            cactus.draw()
        if flag == "b":
            berd.draw()
        if game_over:
            show_game_over()
            dino.draw_die()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
