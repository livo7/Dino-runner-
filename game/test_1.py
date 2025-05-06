import pygame
import random

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Google dino")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Динозавр
dino_img = pygame.Surface((50, 50))
dino_img.fill(BLACK)
dino_rect = dino_img.get_rect(midbottom=(100, 350))
dino_gravity = 0
is_jumping = False

# Кактус
cactus_img = pygame.Surface((30, 50))
cactus_img.fill(BLACK)
cactus_rect = cactus_img.get_rect(midbottom=(900, 350))
cactus_speed = 5

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                dino_gravity = -15
                is_jumping = True

    # Гравитация для динозавра
    dino_gravity += 0.8
    dino_rect.y += dino_gravity
    if dino_rect.bottom >= 350:
        dino_rect.bottom = 350
        is_jumping = False

    # Движение кактуса
    cactus_rect.x -= cactus_speed
    if cactus_rect.right < 0:
        cactus_rect.left = 800
        cactus_rect.height = random.randint(30, 60)

    # Коллизия
    if dino_rect.colliderect(cactus_rect):
        print("Game Over!")
        running = False

    # Отрисовка
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, dino_rect)
    pygame.draw.rect(screen, BLACK, cactus_rect)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
