import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = position
        self.lifetime = 0.4  # seconds
        self.time = 0
        self.radius = 10
        self.max_radius = 60

    def update(self, dt):
        self.time += dt
        if self.time >= self.lifetime:
            self.kill()
        
    def draw(self, screen):
        progress = self.time / self.lifetime
        current_radius = int(self.radius + (self.max_radius - self.radius) * progress)
        alpha = int(255 * (1 - progress))
        
        # Draw multiple circles for a simple explosion effect
        color1 = (255, 0, 0, alpha)
        color2 = (255, 165, 0, alpha)
        color3 = (255, 255, 0, alpha)

        # To draw with alpha, we need a temporary surface
        target_rect = pygame.Rect(self.position.x - current_radius, self.position.y - current_radius, current_radius * 2, current_radius * 2)
        surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        
        pygame.draw.circle(surface, color1, (current_radius, current_radius), current_radius)
        pygame.draw.circle(surface, color2, (current_radius, current_radius), int(current_radius * 0.7))
        pygame.draw.circle(surface, color3, (current_radius, current_radius), int(current_radius * 0.4))
        
        screen.blit(surface, target_rect.topleft)
