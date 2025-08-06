import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = position
        self.lifetime = 0.6  # seconds
        self.time = 0
        self.radius = 10
        self.max_radius = 80
        
        # Add particles to global particle system
        from main import particle_system
        if particle_system:
            particle_system.add_explosion(position)

    def update(self, dt):
        self.time += dt
        if self.time >= self.lifetime:
            self.kill()
        
    def draw(self, screen):
        progress = self.time / self.lifetime
        current_radius = int(self.radius + (self.max_radius - self.radius) * progress)
        alpha = int(255 * (1 - progress))
        
        # Draw multiple circles for a simple explosion effect
        colors = [
            (255, 0, 0, alpha),
            (255, 165, 0, alpha), 
            (255, 255, 0, alpha)
        ]

        # Simple circle explosion without alpha blending
        for i, color in enumerate(colors):
            radius = int(current_radius * (1 - i * 0.3))
            if radius > 0:
                pygame.draw.circle(screen, color[:3], self.position, radius, 2)
