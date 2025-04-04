import pygame, sys
from pygame.locals import *
import random, time

# Initializing 
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0  # Счетчик собранных монет
ENEMY_SPEED_INCREMENT = 5  # Число монет для увеличения скорости врагов

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

# Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

pygame.mixer.music.load("backround.wav")  # Замените на имя вашего файла с музыкой
pygame.mixer.music.play(-1, 0.0)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:  # Если враг выходит за пределы экрана
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Coin class (новый класс для монет)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")  # Путь к изображению монеты
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(-600, -50))  # Случайное появление монеты на экране
        
        # Генерация случайного веса монеты
        self.weight = random.randint(1, 3)  # Веса от 1 до 3

    def move(self):
        global COINS_COLLECTED
        self.rect.move_ip(0, SPEED)  # Двигаем монету вниз
        if self.rect.top > 600:  # Если монета выходит за пределы экрана
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-600, -50))  # Появляется новая монета в случайном месте

# Setting up Sprites        
P1 = Player()
E1 = Enemy()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()  # Группа монет
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Random coin spawning event
COIN_SPAWN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(COIN_SPAWN_EVENT, 2000)  # Спавн монет каждые 2 секунды

# Game Loop
while True:
    # Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5     
        if event.type == COIN_SPAWN_EVENT:
            # Randomly spawn a new coin
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    
    # Display the score and the number of collected coins in the top-right corner
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_display = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_display, (SCREEN_WIDTH - 100, 10))  # Отображаем количество монет в правом верхнем углу

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        

    # Check if player collects any coins
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)  # Пытаемся найти монеты, с которыми столкнулся игрок
    for coin in collected_coins:
        COINS_COLLECTED += coin.weight  # Увеличиваем счетчик монет в зависимости от их веса
        coin.kill()  # Убираем монету из игры

    # Increase enemy speed after collecting N coins
    if COINS_COLLECTED >= ENEMY_SPEED_INCREMENT:
        SPEED += 0.5  # Увеличиваем скорость врагов
        ENEMY_SPEED_INCREMENT += 5  # Увеличиваем порог для следующего увеличения скорости

    pygame.display.update()
    FramePerSec.tick(FPS)