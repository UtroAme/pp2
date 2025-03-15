'''micky mouse clock'''
#library
import pygame
import datetime

def blitRotate(surf, image, center, angle):
        '''function rotate'''        
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=center)
        surf.blit(rotated_image, new_rect.topleft)
  
    
'''Head'''
pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False
clock = pygame.time.Clock()
center = (400,300)
running = True

#pictures
background = pygame.image.load("lab7\pictures\clock.png").convert_alpha()
minute_hand = pygame.image.load("lab7\pictures\min_hand.png").convert_alpha()
second_hand = pygame.image.load("lab7\pictures\sec_hand.png").convert_alpha()


#background = "C:\Users\AS\Desktop\kbtu\pp2\lab7\pictures\clock.png"
#sec = "C:\Users\AS\Desktop\kbtu\pp2\lab7\pictures\sec_hand.png"  x = 440, y = 285
#min = "C:\Users\AS\Desktop\kbtu\pp2\lab7\pictures\min_hand.png"   x = 357, y = 292

while not done:
        '''обработка событий'''
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        #Tacking the time        
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second
  
        #Tacking the angle
        minute_angle = - (minutes * 6)
        second_angle = - (seconds * 6)


        #background
        screen.blit(background, (0,0))

        #arrows
        blitRotate(screen, minute_hand, center, minute_angle)
        blitRotate(screen, second_hand, center, second_angle)

        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()