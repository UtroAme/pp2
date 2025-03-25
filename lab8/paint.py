import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    tool = 'brush'  # Default tool
    drawing = False
    start_pos = None
    
    while True:
        
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                #collors
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                #фигуры    
                elif event.key == pygame.K_q:
                    tool = 'rectangle'
                elif event.key == pygame.K_w:
                    tool = 'circle'
                #tools
                elif event.key == pygame.K_1:
                    tool = 'eraser'
                elif event.key == pygame.K_2:
                    tool = 'brush'
            
            #for event
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = event.pos
                drawing = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if tool in ['rectangle', 'circle'] and start_pos:
                    end_pos = event.pos
                    if tool == 'rectangle':
                        pygame.draw.rect(screen, get_color(mode), pygame.Rect(*start_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), 2)
                    elif tool == 'circle':
                        radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                        pygame.draw.circle(screen, get_color(mode), start_pos, radius, 2)
                drawing = False
                start_pos = None
            
            if event.type == pygame.MOUSEMOTION and drawing and tool in ['brush', 'eraser']:
                color = (0, 0, 0) if tool == 'eraser' else get_color(mode)
                pygame.draw.circle(screen, color, event.pos, radius)

             # Display tool instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "R - Red", "G - Green", "B - Blue", "T - Rectangle", "C - Circle", 
            "E - Eraser", "P - Brush", "ESC - Exit"
        ]
        for i, text in enumerate(instructions):
            screen.blit(font.render(text, True, (255, 255, 255)), (10, 440 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)

def get_color(mode):
    colors = {'blue': (0, 0, 255), 'red': (255, 0, 0), 'green': (0, 255, 0)}
    return colors.get(mode, (255, 255, 255))

main()
