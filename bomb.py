import pygame
from circleshape import CircleShape

class Bomb(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.velocity = pygame.Vector2(0, 0)
        self.lifetime = 3.0  # Explodes after 3 seconds
        self.time = 0
        self.exploded = False

    def draw(self, screen):
        # Flashing bomb
        flash_rate = 10 if self.time > 2.0 else 5
        if int(self.time * flash_rate) % 2 == 0:
            pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)
        else:
            pygame.draw.circle(screen, (255, 100, 100), self.position, self.radius)

    def update(self, dt):
        self.time += dt
        self.position += self.velocity * dt
        self.wrap_around_screen()
        
        if self.time >= self.lifetime and not self.exploded:
            self.explode()

    def explode(self):
        self.exploded = True
        # Create a large explosion effect
        from explosion import Explosion
        Explosion(self.position)
        self.kill()
        return self.position  # Return position for damage calculation
