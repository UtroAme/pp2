#imports
import pygame, sys
from pygame.locals import *
import random, time
 
#initializing
pygame.init()

#setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0
COIN_SPEED = 5
COINS_REQUER = 10
RUN = True

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK) #создание графики для шрифта

background = pygame.image.load("lab9-beta/racer/AnimatedStreet.png")
 
#creating a white screen
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("lab9-beta/racer/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0)  #случайные точки появления
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED) #перемещает на несколько пикселей вниз
        if (self.rect.bottom > 600): #при достижении вниза
            SCORE += 1
            self.rect.top = 0 #отправляет наверх
            self.rect.center = (random.randint(30, 370), 0) #в рандомное место
 
      def draw(self, surface):
        surface.blit(self.image, self.rect) 

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab9-beta/racer/coin.png")
        self.weight = random.randint(1,3)
        self.image = pygame.transform.scale(self.image,(15*self.weight,15*self.weight))
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0)

    def move(self):
        self.rect.move_ip(0,COIN_SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
 
class Player(pygame.sprite.Sprite): #делает Player дочерник классом
    def __init__(self): 
        super().__init__() #для Sprite 
        self.image = pygame.image.load("lab9-beta/racer/Player.png") #передает картину
        self.rect = self.image.get_rect() #создает прямоугольник с размером изображения
        self.rect.center = (160, 520) #определяет начальную поицую rect
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        #if self.rect.top < 0:
         # if pressed_keys[K_UP]:
          #    self.rect.move_ip(0, -5)
        #if self.rect.bottom > SCREEN_HEIGHT:
         # if pressed_keys[K_DOWN]:
          #     self.rect.move_ip(0,5)
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)  #1:картина 2:обьект кударисуем
 
def add_coin():
    if len(money) < 3 and random.randint(1, 100) > 98:  # Ограничение на количество монет и шанс появлния
        new_coin = Coin()
        money.add(new_coin)
        all_sprites.add(new_coin)

def add_enemy():
    if len(enemies) < 1:
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

#Setting up sprites     
P1 = Player()
E1 = Enemy()
new_coin = Coin()

#creating sprites group классификация
enemies = pygame.sprite.Group() #создание группы
enemies.add(E1) #добавление в группу
money = pygame.sprite.Group()
money.add(new_coin)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(new_coin)

#adding a new User event 
INC_SPEED = pygame.USEREVENT + 1 
pygame.time.set_timer(INC_SPEED, 1000) #вызывает обьект каждые 1000миллисек= 1 сек
 
#game loop
while RUN:    
    #Cycles throught all events occuring 
    for event in pygame.event.get():    
        if event.type == INC_SPEED and COINS % COINS_REQUER == 0 and COINS > 0: #увеличивает скрость со временем
            SPEED += 2          
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    DISPLAYSURF.blit(background, (0,0)) #рисует фон
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coins, (300,10))

    #adding coins
    add_coin()


    
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect) #отображаем с помощью blit
        entity.move()

    #coins collision and coin score
    if pygame.sprite.spritecollideany(P1, money):
        collected_coins = pygame.sprite.spritecollide(P1, money, True)
        for coin in collected_coins:
          COINS += coin.weight

 
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies): #второй должен быть ene,y или all_sprites
          pygame.mixer.Sound('lab9-beta/racer/crash.wav').play() #добовляет и воспроизводит звук
          time.sleep(0.5)
          collision_enemy = pygame.sprite.spritecollide(P1, enemies, True)
          COINS -= 1
          add_enemy()

    if COINS < 0:
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
          
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() #удалит спрайт из группы
        time.sleep(2)
        pygame.quit()
        sys.exit() 
         
    pygame.display.update()
    FramePerSec.tick(FPS)