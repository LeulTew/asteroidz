import pygame
import random
import math
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from explosion import Explosion

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Generate lumpy shape points
        self.points = []
        num_points = random.randint(8, 12)
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            # Add random variation to radius for lumpy shape
            variation = random.uniform(0.7, 1.3)
            point_radius = self.radius * variation
            x_offset = math.cos(angle) * point_radius
            y_offset = math.sin(angle) * point_radius
            self.points.append((x_offset, y_offset))

    def draw(self, screen):
        # Draw lumpy asteroid using polygon
        world_points = []
        for point in self.points:
            world_x = self.position.x + point[0]
            world_y = self.position.y + point[1]
            world_points.append((world_x, world_y))
        
        if len(world_points) >= 3:
            pygame.draw.polygon(screen, (128, 128, 128), world_points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_around_screen()

    def split(self):
        Explosion(self.position)
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 30 # Score for small asteroid
        # Split into two smaller asteroids
        random_angle = random.uniform(20, 50)
        vel1 = self.velocity.rotate(random_angle) * 1.2
        vel2 = self.velocity.rotate(-random_angle) * 1.2
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        Asteroid(self.position.x, self.position.y, new_radius).velocity = vel1
        Asteroid(self.position.x, self.position.y, new_radius).velocity = vel2
        if self.radius > ASTEROID_MIN_RADIUS * 2:
             return 10 # Score for large asteroid
        return 20 # Score for medium asteroid