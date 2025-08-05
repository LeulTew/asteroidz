import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (128, 128, 128), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        # Split into two smaller asteroids
        random_angle = random.uniform(20, 50)
        vel1 = self.velocity.rotate(random_angle) * 1.2
        vel2 = self.velocity.rotate(-random_angle) * 1.2
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        Asteroid(self.position.x, self.position.y, new_radius).velocity = vel1
        Asteroid(self.position.x, self.position.y, new_radius).velocity = vel2