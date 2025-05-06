import pygame
import sys
import random

# Инициализация Pygame
try:
    pygame.init()
except pygame.error as e:
    print(f"Ошибка при инициализации Pygame: {e}")
    sys.exit(1)

# Настройки окна
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Шрифт (обработка ошибки, если шрифт не загрузится)
try:
    font = pygame.font.Font(None, 36)
except:
    font = pygame.font.SysFont("arial", 36)


class Dino:
    def __init__(self):
        self.rect = pygame.Rect(100, 350, 50, 50)
        self.gravity = 0
        self.is_jumping = False

    def update(self):
        self.gravity += 0.8
        self.rect.y += self.gravity
        if self.rect.bottom >= 350:
            self.rect.bottom = 350
            self.is_jumping = False

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)


class Cactus:
    def __init__(self):
        self.rect = pygame.Rect(900, 150, 30, 50)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.height = random.randint(30, 60)

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)


def show_game_over():
    text = font.render("Game Over! Нажми R для рестарта", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))


def main():
    dino = Dino()
    cactus = Cactus()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dino.is_jumping and not game_over:
                    dino.gravity = -15
                    dino.is_jumping = True
                if event.key == pygame.K_r and game_over:
                    # Рестарт игры
                    main()
                    return

        if not game_over:
            dino.update()
            cactus.update()

            # Проверка коллизии
            if dino.rect.colliderect(cactus.rect):
                game_over = True

        # Отрисовка
        screen.fill(WHITE)
        dino.draw()
        cactus.draw()

        if game_over:
            show_game_over()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        pygame.quit()
        sys.exit(1)
