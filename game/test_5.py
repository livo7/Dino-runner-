import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
screen_width = 1800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Runner")

# Цвета и шрифты
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (200, 200, 200)
GRAY = (83, 83, 83)
font = pygame.font.Font(None, 36)

# Параметры земли
ground_height = 100
ground_y = screen_height - ground_height


class Dino:
    def __init__(self):
        self.image = pygame.image.load("dino0000.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(midbottom=(100, ground_y))
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
    speed_increase = 0.005  # Постепенное ускорение

    def __init__(self):
        self.type = random.choice(["small", "large", "group"])
        self.setup_cactus()
        self.speed = self.BASE_SPEED
        self.x = screen_width

    def setup_cactus(self):
        if self.type == "small":
            self.width, self.height = 40, 80
            self.rect = pygame.Rect(0, 0, self.width, self.height)
        elif self.type == "large":
            self.width, self.height = 60, 120
            self.rect = pygame.Rect(0, 0, self.width, self.height)
        else:  # group
            self.width, self.height = 180, 80
            self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.midbottom = (self.x, ground_y)

    def update(self, score):
        self.speed = self.BASE_SPEED + score * self.speed_increase
        self.x -= self.speed
        self.rect.midbottom = (self.x, ground_y)
        return self.x + self.width < 0  # Возвращает True, если кактус ушел за экран

    def draw(self):
        if self.type == "group":
            # Рисуем группу из 3 маленьких кактусов
            for i in range(3):
                cactus_rect = pygame.Rect(self.x + i * 60, ground_y - 80, 40, 80)
                pygame.draw.rect(screen, BLACK, cactus_rect)
        else:
            pygame.draw.rect(screen, BLACK, self.rect)


def background():
    screen.fill(WHITE)
    pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, screen_width, ground_height))


def show_score(score):
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(score_text, (screen_width - 200, 50))


def main():
    dino = Dino()
    cacti = []
    last_cactus_time = 0
    cactus_interval = 1500  # Интервал в миллисекундах
    score = 0
    game_over = False

    clock = pygame.time.Clock()
    last_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dino.jump and not game_over:
                    dino.gravity = -20
                    dino.jump = True
                if event.key == pygame.K_r and game_over:
                    main()
                    return

        if not game_over:
            # Генерация кактусов
            if current_time - last_cactus_time > cactus_interval:
                cacti.append(Cactus())
                last_cactus_time = current_time
                cactus_interval = random.randint(1000, 2500)  # Случайный интервал

            # Обновление
            dino.update()
            score += delta_time / 1000  # Увеличиваем счет на основе времени

            # Удаление кактусов за экраном и проверка коллизий
            for cactus in cacti[:]:
                if cactus.update(score):
                    cacti.remove(cactus)
                elif dino.rect.colliderect(cactus.rect):
                    game_over = True

        # Отрисовка
        background()
        dino.draw()
        for cactus in cacti:
            cactus.draw()
        show_score(score)

        if game_over:
            game_over_text = font.render("Game Over! Press R to restart", True, GRAY)
            screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
