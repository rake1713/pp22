import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    color_mode = 'blue'  # Изначально режим - синий цвет
    drawing_mode = 'line'  # Стартовый режим рисования (линии)
    points = []
    erase_radius = 15  # Радиус ластика
    last_pos = None  # Переменная для отслеживания последней точки

    # Цвета кнопок
    button_color = (200, 200, 200)
    selected_button_color = (150, 150, 150)

    while True:
        
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
            # Если нажата кнопка закрытия окна
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Обработка нажатий на кнопки
                if event.button == 1:
                    # Выбор цвета
                    if 10 < event.pos[0] < 110 and 10 < event.pos[1] < 50:  # Красная кнопка
                        color_mode = 'red'
                    elif 120 < event.pos[0] < 220 and 10 < event.pos[1] < 50:  # Зеленая кнопка
                        color_mode = 'green'
                    elif 230 < event.pos[0] < 330 and 10 < event.pos[1] < 50:  # Синяя кнопка
                        color_mode = 'blue'
                    
                    # Выбор режима рисования
                    elif 10 < event.pos[0] < 110 and 60 < event.pos[1] < 100:  # Линия
                        drawing_mode = 'line'
                    elif 120 < event.pos[0] < 220 and 60 < event.pos[1] < 100:  # Круг
                        drawing_mode = 'circle'
                    elif 230 < event.pos[0] < 330 and 60 < event.pos[1] < 100:  # Прямоугольник
                        drawing_mode = 'rect'
                    elif 10 < event.pos[0] < 110 and 110 < event.pos[1] < 150:  # Ластик
                        drawing_mode = 'eraser'
                    # Кнопка для квадрата
                    elif 120 < event.pos[0] < 220 and 110 < event.pos[1] < 150:  # Квадрат
                        drawing_mode = 'square'
                    # Кнопка для прямоугольного треугольника
                    elif 230 < event.pos[0] < 330 and 110 < event.pos[1] < 150:  # Прямоугольный треугольник
                        drawing_mode = 'right_triangle'
                    # Кнопка для равностороннего треугольника
                    elif 10 < event.pos[0] < 110 and 160 < event.pos[1] < 200:  # Равносторонний треугольник
                        drawing_mode = 'equilateral_triangle'
                    # Кнопка для ромба
                    elif 120 < event.pos[0] < 220 and 160 < event.pos[1] < 200:  # Ромб
                        drawing_mode = 'diamond'

                # Левая кнопка - рисовать, если не в пределах кнопок
                if event.button == 1:
                    # Проверка, не в области кнопок
                    if not (10 < event.pos[0] < 330 and 10 < event.pos[1] < 200):
                        if drawing_mode == 'eraser':
                            points = [point for point in points if not is_near(event.pos, point[0], erase_radius)]
                        else:
                            if drawing_mode == 'line' and last_pos is not None:
                                points.append((event.pos, color_mode, drawing_mode, last_pos))
                            else:
                                points.append((event.pos, color_mode, drawing_mode))

                        last_pos = event.pos  # Сохраняем текущую точку как последнюю

            if event.type == pygame.MOUSEMOTION:
                pass

        screen.fill((0, 0, 0))  # Очистка экрана

        # Рисование кнопок
        pygame.draw.rect(screen, selected_button_color if color_mode == 'red' else button_color, pygame.Rect(10, 10, 100, 40))  # Красная
        pygame.draw.rect(screen, selected_button_color if color_mode == 'green' else button_color, pygame.Rect(120, 10, 100, 40))  # Зеленая
        pygame.draw.rect(screen, selected_button_color if color_mode == 'blue' else button_color, pygame.Rect(230, 10, 100, 40))  # Синяя

        pygame.draw.rect(screen, selected_button_color if drawing_mode == 'line' else button_color, pygame.Rect(10, 60, 100, 40))  # Линия
        pygame.draw.rect(screen, selected_button_color if drawing_mode == 'circle' else button_color, pygame.Rect(120, 60, 100, 40))  # Круг
        pygame.draw.rect(screen, selected_button_color if drawing_mode == 'rect' else button_color, pygame.Rect(230, 60, 100, 40))  # Прямоугольник
        pygame.draw.rect(screen, selected_button_color if drawing_mode == 'eraser' else button_color, pygame.Rect(10, 110, 100, 40))  # Ластик
        pygame.draw.rect(screen, selected_button_color if drawing_mode == 'square' else button_color, pygame.Rect(120, 110, 100, 40))  # Квадрат
        pygame.draw.rect(screen, selected_button_color if drawing_mode == 'right_triangle' else button_color, pygame.Rect(230, 110, 100, 40))  # Прямоугольный треугольник
        pygame.draw.rect(screen, selected_button_color if drawing_mode == 'equilateral_triangle' else button_color, pygame.Rect(10, 160, 100, 40))  # Равносторонний треугольник
        pygame.draw.rect(screen, selected_button_color if drawing_mode == 'diamond' else button_color, pygame.Rect(120, 160, 100, 40))  # Ромб

        # Отображение текста на кнопках
        font = pygame.font.SysFont('Arial', 16)
        screen.blit(font.render('КРАСНЫЙ', True, (255, 255, 255)), (25, 20))
        screen.blit(font.render('ЗЕЛЕНЫЙ', True, (255, 255, 255)), (135, 20))
        screen.blit(font.render('СИНИЙ', True, (255, 255, 255)), (250, 20))
        screen.blit(font.render('ЛИНИЯ', True, (255, 255, 255)), (30, 70))
        screen.blit(font.render('КРУГ', True, (255, 255, 255)), (150, 70))
        screen.blit(font.render('ПРЯМОУГОЛЬНИК', True, (255, 255, 255)), (230, 70))
        screen.blit(font.render('ЛАСТИК', True, (255, 255, 255)), (20, 120))
        screen.blit(font.render('КВАДРАТ', True, (255, 255, 255)), (135, 120))
        screen.blit(font.render('ТРЕУГОЛЬНИК', True, (255, 255, 255)), (150, 160))
        screen.blit(font.render('РОМБ', True, (255, 255, 255)), (230, 160))

        # Рисование всех точек
        for point, color, mode, *last in points:
            if mode == 'line' and last:
                pygame.draw.line(screen, get_color(color), last[0], point, radius)  # Рисуем линию между точками
            elif mode == 'circle':
                pygame.draw.circle(screen, get_color(color), point, radius)
            elif mode == 'rect':
                pygame.draw.rect(screen, get_color(color), pygame.Rect(point[0] - radius, point[1] - radius, radius *3, radius * 2))  # Прямоугольник
            elif mode == 'square':
                pygame.draw.rect(screen, get_color(color), pygame.Rect(point[0] - radius, point[1] - radius, radius * 2, radius * 2))  # Квадрат
            elif mode == 'right_triangle':
                draw_right_triangle(screen, point, radius, get_color(color))  # Прямоугольный треугольник
            elif mode == 'equilateral_triangle':
                draw_equilateral_triangle(screen, point, radius, get_color(color))  # Равносторонний треугольник
            elif mode == 'diamond':
                draw_diamond(screen, point, radius, get_color(color))  # Ромб
            elif mode == 'eraser':
                pygame.draw.circle(screen, (255, 255, 255), point, radius)

        pygame.display.flip()
        
        clock.tick(60)

# Проверка, находится ли точка в пределах радиуса
def is_near(pos1, pos2, radius):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 <= radius ** 2

# Получение цвета по текущему режиму
def get_color(mode):
    if mode == 'blue':
        return (0, 0, 255)
    elif mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)
    return (255, 255, 255)  # Белый цвет по умолчанию

# Функция для рисования прямоугольного треугольника
def draw_right_triangle(screen, pos, size, color):
    points = [(pos[0], pos[1]), (pos[0] + size, pos[1]), (pos[0], pos[1] + size)]
    pygame.draw.polygon(screen, color, points)

# Функция для рисования равностороннего треугольника
def draw_equilateral_triangle(screen, pos, size, color):
    height = (3 ** 0.5 / 2) * size  # Высота равностороннего треугольника
    points = [(pos[0], pos[1]), 
              (pos[0] + size, pos[1]), 
              (pos[0] + size / 2, pos[1] - height)]
    pygame.draw.polygon(screen, color, points)

# Функция для рисования ромба
def draw_diamond(screen, pos, size, color):
    points = [(pos[0], pos[1] - size), 
              (pos[0] + size, pos[1]), 
              (pos[0], pos[1] + size), 
              (pos[0] - size, pos[1])]
    pygame.draw.polygon(screen, color, points)

if __name__ == "__main__":
    main()