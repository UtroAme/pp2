#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_COUNT = 0
COIN_REQUEST = 10

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("lab8&9/racer_resource/AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("lab8&9/racer_resource/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.randint(1, 3)  # Assigning random weight (1-3)
        size = 15 * self.weight  # Making bigger coins based on weight
        self.image = pygame.image.load("lab8&9/racer_resource/coin.png")
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        """Moves the coin to a new random position."""
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), 
                             random.randint(200, SCREEN_HEIGHT - self.rect.height))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("lab8&9/racer_resource/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.speed = 5
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-self.speed, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(self.speed, 0)
        if self.rect.top > 0:
               if pressed_keys[K_UP]:
                    self.rect.move_ip(0,-self.speed)
        if self.rect.bottom < SCREEN_HEIGHT:
               if pressed_keys[K_DOWN]:
                    self.rect.move_ip(0,self.speed)
                  

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group()

#create multiple coins
for _ in range(3):
     coins.add(Coin())

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, *coins)
all_sprites.add(*coins)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED and COIN_COUNT % COIN_REQUEST == 0 and COIN_COUNT > 0:
              SPEED += 1.5    
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    # Draw background
    DISPLAYSURF.blit(background, (0,0))

    # Display score and coin count
    score_display = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_display = font_small.render(f"Coins: {COIN_COUNT}", True, BLACK)
    DISPLAYSURF.blit(score_display, (10, 10))
    DISPLAYSURF.blit(coin_display, (SCREEN_WIDTH - 100, 10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        if isinstance(entity ,Player) or isinstance(entity, Enemy):
             entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check coin collisions
    collected_coins = pygame.sprite.spritecollide(P1, coins, dokill=True)
    for coin in collected_coins:
        COIN_COUNT += coin.weight  # add coin's weight to count
        new_coin = Coin()
        coins.add(new_coin) #respawn coin
        all_sprites.add(new_coin)

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('lab8&9/racer_resource/crash.wav').play()
          time.sleep(1)
                   
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)
