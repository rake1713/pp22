import pygame
import time
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Часы Микки Мауса")

# Загрузка изображения часов
clock_image = pygame.image.load("mickeyclock.jpeg")  # Используй свою картинку
clock_image = pygame.transform.scale(clock_image, (WIDTH, HEIGHT))

# Центр часов
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Функция для рисования стрелок
def draw_hand(angle, length, color, thickness):
    """Рисует стрелку, вращая её на заданный угол"""
    end_x = center_x + length * math.cos(math.radians(angle))
    end_y = center_y - length * math.sin(math.radians(angle))
    pygame.draw.line(screen, color, (center_x, center_y), (end_x, end_y), thickness)

# Основной цикл
running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(clock_image, (0, 0))

    # Получаем текущее время
    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    # Углы для минутной и секундной стрелки
    minute_angle = 90 - (minutes * 6)  # 360 градусов / 60 минут
    second_angle = 90 - (seconds * 6)  # 360 градусов / 60 секунд

    # Рисуем стрелки
    draw_hand(minute_angle, 100, (0, 0, 0), 8)  # Минутная стрелка (чёрная)
    draw_hand(second_angle, 120, (255, 0, 0), 4)  # Секундная стрелка (красная)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.time.delay(100)

pygame.quit()