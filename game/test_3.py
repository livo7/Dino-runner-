import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Runner")
clock = pygame.time.Clock()
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (240, 240, 240)  # Светло-серый для земли
SKY_COLOR = (135, 206, 235)  # Голубой для неба

# Параметры земли
GROUND_HEIGHT = 100
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT


class Dino:
    def __init__(self):
        self.width = 60
        self.height = 80
        self.x = 100
        self.y = GROUND_Y - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.gravity = 0
        self.is_jumping = False
        self.run_animation_count = 0
        self.run_sprites = [
            pygame.Rect(self.x, self.y, self.width, self.height),
            pygame.Rect(self.x, self.y + 10, self.width, self.height - 10),
        ]

    def update(self):
        # Гравитация
        self.gravity += 0.8
        self.rect.y += self.gravity

        # Ограничение на земле
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.is_jumping = False

        # Анимация бега
        if not self.is_jumping:
            self.run_animation_count = (self.run_animation_count + 0.1) % 2

    def draw(self):
        # Рисуем динозавра (простая анимация бега)
        current_sprite = self.run_sprites[int(self.run_animation_count)]
        pygame.draw.rect(screen, BLACK, current_sprite)


def draw_background():
    # Небо
    screen.fill(SKY_COLOR)
    # Земля
    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))
    # Линия горизонта
    pygame.draw.line(screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)


def main():
    dino = Dino()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dino.is_jumping:
                    dino.gravity = -15
                    dino.is_jumping = True

        # Обновление
        dino.update()

        # Отрисовка
        draw_background()
        dino.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
