#imports
import pygame, sys
from pygame.locals import *
import random, time

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

pygame.quit()