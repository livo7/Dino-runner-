import pygame
import sys
import os

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
GROUND_COLOR = (240, 240, 240)
SKY_COLOR = (135, 206, 235)

# Параметры земли
GROUND_HEIGHT = 100
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT


class Dino:
    def __init__(self):
        # Загрузка изображения
        try:
            self.image = pygame.image.load("dino0000.png").convert_alpha()
            # Масштабирование (если нужно)
            self.image = pygame.transform.scale(self.image, (60, 80))
        except:
            print("Ошибка загрузки изображения! Будет использован прямоугольник")
            self.image = None

        self.rect = pygame.Rect(100, GROUND_Y - 80, 60, 80)
        self.gravity = 0
        self.is_jumping = False
        self.animation_count = 0
        self.run_images = [
            "dinorun0000.png",
            "dinorun0001.png",
        ]  # Сюда можно добавить разные кадры анимации

    def update(self):
        self.gravity += 0.8
        self.rect.y += self.gravity

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.is_jumping = False

        # Анимация бега
        if not self.is_jumping:
            self.animation_count = (self.animation_count + 0.1) % 2

    def draw(self):
        if self.image:
            # Рисуем изображение
            screen.blit(self.image, self.rect)
        else:
            # Запасной вариант - прямоугольник
            pygame.draw.rect(screen, (0, 0, 0), self.rect)


def draw_background():
    screen.fill(SKY_COLOR)
    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))
    pygame.draw.line(screen, (0, 0, 0), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)


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

        dino.update()
        draw_background()
        dino.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
