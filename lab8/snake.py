'''snake game'''
import pygame
import random

pygame.init()

width = 600
heght = 600
screen = pygame.display.set_mode((width,heght))
cell = 30

done = False
score = 0
level = 1
FPS = 5
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

#background
def draw_grid():
    for i in range(heght//cell):
        for j in range(width//cell):
            pygame.draw.rect(screen, (100,100,100), (i * cell, j * cell, cell, cell))
    
def draw_grid_chess():
    colors = [(255,255,255), (100,100,100)]

    for i in range(heght//cell):
        for j in range(width//cell):
            pygame.draw.rect(screen, colors[(i+j)%2],(i*cell, j*cell, cell, cell))

#variables
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y= y

    
class Snake:
    def __init__(self):
        self.body = [Point(10,11),Point(10,12),Point(10,13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        '''for i in range(len(self.body) -1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy'''

        new_head = Point(self.body[0].x + self.dx, self.body[0].y + self.dy)
        
        #Перемецение змеки на границе
        new_head.x %= width // cell
        new_head.y %= heght // cell

        #chek for body and head столкновения
        for segment in self.body:
            if new_head.x == segment.x and new_head.y == segment.y:
                global done
                done = True
                return

        self.body.insert(0,new_head)
        self.body.pop()

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, (255,0,0), (head.x * cell, head.y * cell, cell, cell))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, (0,255,0), (segment.x * cell, segment.y * cell, cell, cell))
   
    def check_collision(self, food):
        global score, level, FPS
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            score += 1
            self.body.append(Point(head.x, head.y))
            food.spawn(self)
            if score % 4 == 0:
                level += 1
                FPS += 2

class Food:
    def __init__(self):
        self.pos = Point(9,9)

    def spawn(self, snake):
        while True:
            new_x = random.randint(0, (width // cell) - 1)
            new_y = random.randint(0, (heght // cell) - 1)
            if all(segment.x != new_x or segment != new_y for segment in snake.body):
                self.pos = Point(new_x, new_y)
                break

    def draw(self):
        pygame.draw.rect(screen, (255,255,0), (self.pos.x * cell, self.pos.y * cell, cell ,cell))

food = Food()
snake = Snake()
food.spawn(snake)

#gameplay loop
while not done:
    #gameplay conditions
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

    snake.move()
    snake.check_collision(food)

    snake.draw()
    food.draw()

    #Score and lvl
    score_txt = font.render(f"Score: {score}  Level: {level}", True, (0,0,0))
    screen.blit(score_txt, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)    

pygame.quit()