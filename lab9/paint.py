import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 255, 255))  # fill background with white

# colors
colors = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}
current_color = colors['black'] 

LMBpressed = False 
THICKNESS = 5 #Толщина
tool = 'brush'  # startet tool
start_pos = None

#shape draw
def draw_shape(start, end, shape, color):
    if shape == 'rectangle':
        # use *start to create x,y positions
        pygame.draw.rect(screen, color, pygame.Rect(*start, end[0] - start[0], end[1] - start[1]), THICKNESS)
    elif shape == 'circle':
        #calculate radius use the dist which give us distance between start and end
        radius = int(math.dist(start, end))
        pygame.draw.circle(screen, color, start, radius, THICKNESS)
    elif shape == 'square':
        #calculate the side что бы не стал rectangle 
        side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
        pygame.draw.rect(screen, color, pygame.Rect(start[0], start[1], side, side), THICKNESS)
    elif shape == 'right_triangle':
        '''
        (start[0], start[1]) — верхний угол.
        (start[0], end[1]) — нижний левый угол.
        (end[0], end[1]) — нижний правый угол.
        '''
        pygame.draw.polygon(screen, color, [start, (start[0], end[1]), (end[0], end[1])], THICKNESS)
    elif shape == 'equilateral_triangle':
        '''
        Верхняя (start[0], start[1] - height).
        Левая (start[0] - half_base, start[1]).
        Правая (start[0] + half_base, start[1]).
        '''
        height = abs(end[1] - start[1]) #calculate the hight 
        half_base = height / math.sqrt(3) #высчитываем радиус вписанного кгрука для расчета вершин
        pygame.draw.polygon(screen, color, [(start[0], start[1] - height), (start[0] - half_base, start[1]), (start[0] + half_base, start[1])], THICKNESS)
    elif shape == 'rhombus':
        '''
        Верхняя (center_x, start[1]).
        Правая (end[0], center_y).
        Нижняя (center_x, end[1]).
        Левая (start[0], center_y).
        '''
        center_x = (start[0] + end[0]) // 2
        center_y = (start[1] + end[1]) // 2
        pygame.draw.polygon(screen, color, [(center_x, start[1]), (end[0], center_y), (center_x, end[1]), (start[0], center_y)], THICKNESS)
    elif shape == 'line':
        pygame.draw.line(screen,  color, start, end, THICKNESS)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            start_pos = event.pos
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if LMBpressed and tool == 'brush': #что бы рисовал и при нажатии
                pygame.draw.circle(screen, current_color, (mouse_x, mouse_y), THICKNESS)
            elif LMBpressed and tool == 'eraser': #использует белый цвет как ластик
                pygame.draw.circle(screen, colors['white'], (mouse_x, mouse_y), THICKNESS)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False

            #if we use a shape as tool we draw it with function
            if tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus', 'line'] and start_pos:
                draw_shape(start_pos, event.pos, tool, current_color)
        if event.type == pygame.KEYDOWN:
               #thickness selector
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
                #color selector
            if event.key == pygame.K_r:
                current_color = colors['red']
            if event.key == pygame.K_g:
                current_color = colors['green']
            if event.key == pygame.K_b:
                current_color = colors['blue']
            if event.key == pygame.K_k:
                current_color = colors['black']
                #tools
            if event.key == pygame.K_e:
                tool = 'eraser'
            if event.key == pygame.K_w:
                tool = 'brush'
                #shapes
            if event.key == pygame.K_7:
                tool = 'rectangle'
            if event.key == pygame.K_1:
                tool = 'circle'
            if event.key == pygame.K_2:
                tool = 'square'
            if event.key == pygame.K_3:
                tool = 'right_triangle'
            if event.key == pygame.K_4:
                tool = 'equilateral_triangle'
            if event.key == pygame.K_5:
                tool = 'rhombus'
            if event.key == pygame.K_6:
                tool = 'line'

     # Display tool instructions
        font = pygame.font.Font(None, 28)
        instructions = [
            "R - Red", "G - Green", "B - Blue", "K - Black", "K - Black", "1 - Circle", "2 - Square", "3 - Right triangle", "4 - Equilateral triangle", "5 - Rhombus","6 - Line", "7 - Rectangle"
            ,"E - Eraser", "W - Brush"
        ]
        for i, text in enumerate(instructions):
            screen.blit(font.render(text, True, (0,0,0)), (10, 0 + i * 20))
    
    pygame.display.flip()
pygame.quit()
