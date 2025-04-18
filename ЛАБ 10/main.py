import psycopg2
import pygame
import sys
import random
import time

# Базамен байланыс
conn = psycopg2.connect(
    dbname='rake',
    user='postgres',
    password='2005',  
    host='localhost',
    port='5432'
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        score INTEGER,
        level INTEGER,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()

# Таңдау: жаңа ойыншы ма, ескі ойыншы ма
# Атын сұрау және тексеру
username = input("Атыңды енгіз: ").strip()
user_id = None
score = 0
level = 1


# Қолданушыны тексеру немесе жасау
cur.execute("SELECT id FROM users WHERE username = %s", (username,))
user = cur.fetchone()

if user:
    user_id = user[0]
    cur.execute("SELECT score, level FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
    row = cur.fetchone()
    score = row[0] if row else 0
    level = row[1] if row else 1
    print(f"{username} табылды. {level}-деңгейден бастаймыз.")
else:
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
    print(f"Жаңа қолданушы {username} тіркелді. Ойын 1-деңгейден басталады.")

print("Ойын 5 секундтан кейін басталады...")
time.sleep(5)

# Pygame параметрлері
pygame.init()
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
speed = 10 + level * 2

def generate_food(snake):
    while True:
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        if (x, y) not in snake:
            return (x, y)



def game():
    global score, level, speed
    running = True
    while running:
        # Ойынның бастапқы мәндері
        snake = [(100, 100), (80, 100), (60, 100)]
        direction = (GRID_SIZE, 0)
        food = generate_food(snake)
        speed = 10 + level * 2
        game_over = False

        while not game_over:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cur.close()
                    conn.close()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != (0, GRID_SIZE):
                        direction = (0, -GRID_SIZE)
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != (0, -GRID_SIZE):
                        direction = (0, GRID_SIZE)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != (GRID_SIZE, 0):
                        direction = (-GRID_SIZE, 0)
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != (-GRID_SIZE, 0):
                        direction = (GRID_SIZE, 0)
                    elif event.key == pygame.K_p:
                        paused = True
                        pause_text = font.render(" Пауза - кез келген батырма", True, WHITE)
                        screen.blit(pause_text, (WIDTH // 2 - 180, HEIGHT // 2))
                        pygame.display.flip()
                        cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
                                    (user_id, score, level))
                        conn.commit()
                        print("⏸ Пауза кезінде нәтиже сақталды.")
                        while paused:
                            for pause_event in pygame.event.get():
                                if pause_event.type == pygame.KEYDOWN:
                                    paused = False

            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            if (new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake):
                game_over = True
                break

            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                if score % 3 == 0:
                    level += 1
                    speed += 2
                food = generate_food(snake)
            else:
                snake.pop()

            pygame.draw.rect(screen, RED, (*food, GRID_SIZE, GRID_SIZE))
            for segment in snake:
                pygame.draw.rect(screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))

            score_text = font.render(f"{username} | Ұпай: {score} | Деңгей: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(speed)

        # Ойын соғылғанда: базаға сақтау
        cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
                    (user_id, score, level))
        conn.commit()
        print("Ойын аяқталды. Ұпай базаға сақталды.")

        # Экранда аяқталу экраны
        screen.fill(BLACK)
        over_text = font.render("Game Over!", True, WHITE)
        info_text = font.render(f"Score: {score} | Level: {level}", True, WHITE)
        restart_text = font.render("R - restart | Q - quit", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
        screen.blit(info_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
        pygame.display.flip()

        # R немесе Q пернесін күту
        wait_for_choice = True
        while wait_for_choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    wait_for_choice = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Базадан соңғы нәтижелерді қайта жүктеу
                        cur.execute("SELECT score, level FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
                        row = cur.fetchone()
                        score = row[0] if row else 0
                        level = row[1] if row else 1
                        wait_for_choice = False
                    elif event.key == pygame.K_q:
                        running = False
                        wait_for_choice = False

    pygame.quit()

game()
cur.close()
conn.close()