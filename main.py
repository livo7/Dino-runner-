import pygame
import random
import sys

pygame.init()

# настройка экрана
screen_width = 1800
screen_height = 800
ground_height = 100
ground_y = screen_height - ground_height
FPS = 30

clock = pygame.time.Clock()

try:
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Google_dino")
except pygame.error as e:
    print(f"Ошибка инициализации экрана: {e}")
    sys.exit(1)

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (200, 200, 200)
GRAY = (83, 83, 83)

try:
    font = pygame.font.Font(None, 36)
except pygame.error as e:
    print(f"Ошибка загрузки шрифта: {e}")
    font = pygame.font.SysFont("arial", 36)


class Dino:
    def __init__(self):
        self.normal_size = (100, 100)
        self.current_image = None
        try:
            self.jump_image = pygame.transform.scale(
                pygame.image.load("dinoJump0000.png").convert_alpha(), self.normal_size
            )
            self.run_images = [
                pygame.transform.scale(
                    pygame.image.load("dinorun0000.png").convert_alpha(), self.normal_size
                ),
                pygame.transform.scale(
                    pygame.image.load("dinorun0001.png").convert_alpha(), self.normal_size
                ),
            ]
            self.dead_image = pygame.transform.scale(
                pygame.image.load("dinoDead0000.png").convert_alpha(), self.normal_size
            )
            self.current_image = self.run_images[0]
        except (pygame.error, FileNotFoundError) as e:
            print(f"Ошибка загрузки изображений динозавра: {e}")
            # черные прямоугольники как заглушки
            self.jump_image = pygame.Surface(self.normal_size)
            self.jump_image.fill(BLACK)
            self.run_images = [pygame.Surface(self.normal_size) for _ in range(2)]
            for img in self.run_images:
                img.fill((BLACK))
            self.dead_image = pygame.Surface(self.normal_size)
            self.dead_image.fill(BLACK)

        self.rect = pygame.Rect(100, ground_y, 80, 80)
        self.gravity = 0
        self.jump = False
        self.dead = False
        self.duck = False
        self.animation_count = 0
        self.animation_speed = 0.15

    def update(self):
        if not self.jump and not self.dead:
            self.animation_count += self.animation_speed
            if self.animation_count >= 2:
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
        self.cactus_type = random.randint(1, 3)
        self.image = None
        self.rect = None
        self.setup_cactus()
        self.speed = 15
        self.spawn_delay = random.randint(5, 20)
        self.waiting = True
        self.delay_counter = 0

    def setup_cactus(self):
        try:
            if self.cactus_type == 1:
                self.cactus_width, self.cactus_height = 60, 120
                self.image = pygame.image.load("cactusBig0000.png").convert_alpha()
            elif self.cactus_type == 2:
                self.cactus_width, self.cactus_height = 40, 80
                self.image = pygame.image.load("cactusSmall0000.png").convert_alpha()
            elif self.cactus_type == 3:
                self.cactus_width, self.cactus_height = 120, 80
                self.image = pygame.image.load("cactusSmallMany0000.png").convert_alpha()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Ошибка загрузки кактуса (тип {self.cactus_type}): {e}")
            # черные прямоугольники как заглушки
            self.cactus_width, self.cactus_height = 60, 120
            self.image = pygame.Surface((self.cactus_width, self.cactus_height))
            self.image.fill(BLACK)
            self.rect = self.image.get_rect(bottomleft=(screen_width, ground_y))

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


def background():
    pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, screen_width, screen_height))


def show_game_over():
    try:
        text1 = font.render("Game Over", True, GRAY)
        text1_rect = text1.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
        text2 = font.render("Press ~R~", True, GRAY)
        text2_rect = text2.get_rect(center=(screen_width // 2, screen_height // 2 + 20))

        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
    except Exception as e:
        print(f"Ошибка отображения Game Over: {e}")


def main():
    try:
        dino = Dino()
        cactus = Cactus()
        score = 0
        game_run = True
        game_over = False

        last_time = pygame.time.get_ticks()

        while game_run:
            try:
                current_time = pygame.time.get_ticks()
                delta_time = current_time - last_time
                last_time = current_time

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w and not dino.jump and not game_over:
                            dino.gravity = -20
                            dino.jump = True
                        if event.key == pygame.K_r and game_over:
                            return main()  # рестарт игрыn
                if not game_over:
                    cactus.update()
                    dino.update()
                    score += delta_time / 1000
                    if dino.rect.colliderect(cactus.rect):  # проверка соприкосновения
                        game_over = True
                        dino.draw_die()

                # Отрисовка
                screen.fill(WHITE)
                background()
                dino.draw()
                cactus.draw()

                # Отображение счета
                try:
                    score_text = font.render(f"Score: {int(score)}", True, BLACK)
                    screen.blit(score_text, (screen_width - 200, 50))
                except Exception as e:
                    print(f"Ошибка отображения счета: {e}")

                if game_over:
                    show_game_over()

                pygame.display.update()
                clock.tick(FPS)
            except Exception as e:
                print(f"Ошибка в игровом цикле: {e}")
                game_run = False
    except Exception as e:
        print(f"Критическая ошибка при запуске игры: {e}")
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
