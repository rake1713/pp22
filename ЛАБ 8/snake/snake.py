import pygame
import random

# Инициализация pygame
pygame.init()

# Определяем размеры экрана и цвета
WIDTH, HEIGHT = 640, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Размеры блоков
BLOCK_SIZE = 20

# Создаем экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Шрифт для счета
font = pygame.font.SysFont("Arial", 24)

# Функция для отображения счета и уровня
def display_score_and_level(score, level):
    score_text = font.render(f"Счет: {score}", True, WHITE)
    level_text = font.render(f"Уровень: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

# Функция для создания случайной еды
def random_food():
    return random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE), random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)

# Основной цикл игры
def game():
    clock = pygame.time.Clock()

    # Начальные параметры
    snake_pos = [(100, 100), (90, 100), (80, 100)]  # Позиции змеи
    snake_direction = (BLOCK_SIZE, 0)  # Направление змеи (вправо)
    food_pos = random_food()
    score = 0
    level = 1
    speed = 10  # Начальная скорость
    running = True

    # Основной игровой цикл
    while running:
        screen.fill(BLACK)

        # Проверка событий (например, нажатие клавиш)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake_direction != (0, BLOCK_SIZE):
                    snake_direction = (0, -BLOCK_SIZE)
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake_direction != (0, -BLOCK_SIZE):
                    snake_direction = (0, BLOCK_SIZE)
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake_direction != (BLOCK_SIZE, 0):
                    snake_direction = (-BLOCK_SIZE, 0)
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake_direction != (-BLOCK_SIZE, 0):
                    snake_direction = (BLOCK_SIZE, 0)

        # Перемещение змеи
        new_head = (snake_pos[0][0] + snake_direction[0], snake_pos[0][1] + snake_direction[1])
        snake_pos.insert(0, new_head)

        # Проверка на столкновение с границей
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            running = False  # Игра заканчивается

        # Проверка на столкновение с телом змеи
        if new_head in snake_pos[1:]:
            running = False  # Игра заканчивается

        # Проверка на съедание еды
        if new_head == food_pos:
            score += 1
            if score % 3 == 0:  # Переход на следующий уровень после 3 съеденных ед
                level += 1
                speed += 5  # Увеличиваем скорость при переходе на новый уровень
            food_pos = random_food()
        else:
            snake_pos.pop()  # Удаляем хвост змеи

        # Отображение змеи
        for segment in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        # Отображение еды
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # Отображение счета и уровня
        display_score_and_level(score, level)

        # Обновляем экран
        pygame.display.update()

        # Устанавливаем скорость игры в зависимости от уровня
        clock.tick(speed)

    pygame.quit()

# Запуск игры
game()