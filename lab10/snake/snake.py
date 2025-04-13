#imports
import pygame, sys
from pygame.locals import *
import random, time
import psycopg2
import json
from configparser import ConfigParser

#initializing
pygame.init()

#setting up FPS
FPS = 5
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100,100,100)
 
# Screen information
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

#constant
CELL = 30
FOOD_LIFETIME = 5000 #5s= 500 ms

#Fruit png
fruit1 = pygame.image.load("lab9-beta/snake/blackberry.png")
fruit2 = pygame.image.load("lab9-beta/snake/strawberry.png")
fruit3 = pygame.image.load("lab9-beta/snake/watermelon.png")
fruits = [fruit1, fruit2, fruit3]

#Variables
done = False
SCORE = 0
LEVEL = 1
font = pygame.font.Font(None, 36)

#Background
def draw_grid():
    for i in range(SCREEN_HEIGHT//CELL):
        for j in range(SCREEN_WIDTH//CELL):
            pygame.draw.rect(screen ,GREY, (i*CELL, j*CELL, CELL, CELL))

def draw_grid_chess():
    colors= [WHITE, GREY]

    for i in range(SCREEN_HEIGHT//CELL):
        for j in range(SCREEN_WIDTH//CELL):
            pygame.draw.rect(screen, colors[(i+j)%2], (i*CELL, j*CELL, CELL, CELL))

#connecting database
def load_config(filename='lab10/snake/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        for param in parser.items(section):
            config[param[0]] = param[1]
    return config

def get_db_connection():
    config = load_config()
    return psycopg2.connect(**config)

#ЗАпрос имени
def get_or_create_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    if result:
        user_id = result[0]
        cur.execute("""SELECT score, level, game_state 
                       FROM user_scores 
                       WHERE user_id = %s 
                       ORDER BY last_updated DESC 
                       LIMIT 1""", (user_id,))
        data = cur.fetchone()
        cur.close()
        conn.close()
        return user_id, data
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return user_id, None

def save_game(user_id, score, level, snake_obj):
    conn = get_db_connection()
    cur = conn.cursor()
    # Сохраняем только координаты змейки (game state)
    game_state = json.dumps([{'x': p.x, 'y': p.y} for p in snake_obj.body])
    cur.execute("""
        INSERT INTO user_scores (user_id, score, level, game_state)
        VALUES (%s, %s, %s, %s)
    """, (user_id, score, level, game_state))
    conn.commit()
    cur.close()
    conn.close()

#variable
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10,11),Point(10,12),Point(10,13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        new_head = Point(self.body[0].x + self.dx, self.body[0].y + self.dy)
        
        # Проверка выхода за границы экрана
        if new_head.x < 0 or new_head.x >= SCREEN_WIDTH // CELL or new_head.y < 0 or new_head.y >= SCREEN_HEIGHT // CELL:
            global done
            done = True
            return
        
        #chek for body and head collision
        for segment in self.body:
            if new_head.x == segment.x and new_head.y == segment.y:
                done = True
                return

        self.body.insert(0,new_head)
        self.body.pop()

    def draw(self):
          '''draw snake'''
          head = self.body[0] #head part
          pygame.draw.rect(screen, (255,0,0), (head.x * CELL, head.y * CELL, CELL, CELL))
          for segment in self.body[1:]: #adding the tail
              pygame.draw.rect(screen, (0,255,0), (segment.x * CELL, segment.y * CELL, CELL, CELL))
   
    def check_collision(self, food):
           '''collrction food'''
           global SCORE, LEVEL, FPS
           head = self.body[0]
           if head.x == food.pos.x and head.y == food.pos.y:
              SCORE += food.weight #increase score based on food weight
              self.body.append(Point(head.x, head.y))
              food.spawn(self)
              if SCORE % 4 == 0 and SCORE > 0:
                  LEVEL += 1
                  FPS += 1 #increase speed

class Food:
    def __init__(self):
        self.spawn_time = pygame.time.get_ticks()
        self.spawn(None)

    def spawn(self, snake):
        '''spawn food at random position'''
        self.weight = random.randint(1, 3)
        self.image = pygame.transform.scale(fruits[self.weight-1],(CELL,CELL))
        while True:
            new_x = random.randint(0, (SCREEN_WIDTH // CELL) - 1)
            new_y = random.randint(0, (SCREEN_HEIGHT // CELL) - 1)
            if snake is None or all(segment.x != new_x or segment.y != new_y for segment in snake.body):
                self.pos = Point(new_x, new_y)
                break
        self.spawn_time = pygame.time.get_ticks()

    def draw(self):
         screen.blit(self.image, (self.pos.x * CELL, self.pos.y * CELL))

    def is_expired(self, FOOD_LIFETIME):
        return pygame.time.get_ticks() - self.spawn_time > FOOD_LIFETIME

food = Food()
snake = Snake()
food.spawn(snake)

#запрос на имя и как в дальнейшем игра запуститься
username = input("Enter your username: ")
user_id, saved_data = get_or_create_user(username)

if saved_data:
    SCORE, LEVEL, game_state = saved_data
    print(f"Welcome back {username}! Loaded score: {SCORE}, level: {LEVEL}")
    # Восстановление змеи
    snake = Snake()
    snake.body = [Point(seg['x'], seg['y']) for seg in json.loads(game_state)]
else:
    snake = Snake()

print("Game starts in:")
for i in range(5, 0, -1):
    print(i)
    time.sleep(1)    


#Gaming loop
while not done:
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            if event.key  == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            if event.key  == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            if event.key  == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1 
            if event.key == pygame.K_p: #при нажатии на p у вас будет пауза
              save_game(user_id, SCORE, LEVEL, snake)
              print("Game paused and saved.")
              paused = True
              while paused:
                for pause_event in pygame.event.get():
                    if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_p:
                       paused = False

     #draw background
     draw_grid_chess()

     # Move snake and check collision
     snake.move()
     snake.check_collision(food)

     #check food life time
     if food.is_expired(FOOD_LIFETIME):
         food = Food()
 
     #draw objects
     snake.draw()
     food.draw()


     #Score and lvl
     score_txt = font.render(f"Score: {SCORE}  Level: {LEVEL}", True, (0,0,0))
     screen.blit(score_txt, (10, 10))

     #updating picture
     pygame.display.flip()
     FramePerSec.tick(FPS)
save_game(user_id, SCORE, LEVEL, snake)
pygame.quit()