import pygame

def draw_background(screen):
    """Draws a subtle gradient background."""
    top_color = (10, 20, 40)
    bottom_color = (30, 40, 60)
    
    for y in range(screen.get_height()):
        # Interpolate color from top to bottom
        ratio = y / screen.get_height()
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))
