import pygame

pygame.init()

WIDHT, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDHT,HEIGHT))
pygame.display.set_caption("Paint") #название окна
screen.fill((255,255,255))

#colors
colors = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}
current_color = colors['black'] 

#variables
LMBpressed = False 
THICKNESS = 5 #Толщина
tool = 'brush'  # startet tool
start_pos = None
SQRT_3 = 1.732  
#shape draw function
def draw_shape(start, end, shape, color):
    # Unpack coordinates for clarity
    x1, y1 = start
    x2, y2 = end

    if shape == 'rectangle':
        width = x2 - x1
        height = y2 - y1
        rect = pygame.Rect(x1, y1, width, height)
        pygame.draw.rect(screen, color, rect, THICKNESS)

    elif shape == 'circle':
        # Calculate the radius using the distance formula without math.dist
        radius = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)
        pygame.draw.circle(screen, color, start, radius, THICKNESS)

    elif shape == 'square':
        # Ensure square by using the smaller difference
        side = min(abs(x2 - x1), abs(y2 - y1))
        square = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(screen, color, square, THICKNESS)

    elif shape == 'right_triangle':
        # Triangle with vertices at the top-left, bottom-left, and bottom-right
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(screen, color, points, THICKNESS)

    elif shape == 'equilateral_triangle':
        # Use the vertical difference as height and calculate half of the base
        height = abs(y2 - y1)
        half_base = height / SQRT_3
        points = [(x1, y1 - height), (x1 - half_base, y1), (x1 + half_base, y1)]
        pygame.draw.polygon(screen, color, points, THICKNESS)

    elif shape == 'rhombus':
        # Calculate the center of the shape
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        points = [(center_x, y1), (x2, center_y), (center_x, y2), (x1, center_y)]
        pygame.draw.polygon(screen, color, points, THICKNESS)

    elif shape == 'line':
        pygame.draw.line(screen, color, start, end, THICKNESS)


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
            "R - Red", "G - Green", "B - Blue", "K - Black", "1 - Circle", "2 - Square", "3 - Right triangle", "4 - Equilateral triangle", "5 - Rhombus","6 - Line", "7 - Rectangle"
            ,"E - Eraser", "W - Brush"
        ]
        for i, text in enumerate(instructions):
            screen.blit(font.render(text, True, (0,0,0)), (10, 0 + i * 20))
    
    pygame.display.flip()
pygame.quit()