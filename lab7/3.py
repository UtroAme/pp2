'''Circle follow your mouse'''
import pygame #for download $pip install pygame


'''creating the window'''
pygame.init()
screen = pygame.display.set_mode((400, 300))
'''Adding some static data'''
done = False
is_blue = True
x = 200 #midlle patr of window
y = 150 
r = 25
clock = pygame.time.Clock() #для управления частоты экрана


'''body part'''
while not done:
        '''обработка событий'''
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True



        #movement and limits
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and y > 0+r : y -= 20 #to go up we decrease y
        if pressed[pygame.K_DOWN] and y < 300-r : y +=20 # to go down we increase y 
        if pressed[pygame.K_LEFT] and x > 0+r : x -= 20
        if pressed[pygame.K_RIGHT] and x < 400-r : x += 20

        '''        illuastration 
        (0,0)  --------------------(400,0)
               |                   |
               |                   |
               |                   |
               |                   |
        (0,300)--------------------(400,300)
        '''

        #Background
        screen.fill((255,255,255)) #white background

        #circle
        pygame.draw.circle(screen, (255,0 ,0), (x,y), r)
        
        #updating screen
        pygame.display.flip()
        clock.tick(60)
