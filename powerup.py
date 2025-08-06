import pygame
import random
import math
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

POWERUP_SHIELD = 0
POWERUP_SPEED = 1

class PowerUp(CircleShape):
    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, 15)
        self.powerup_type = powerup_type
        self.lifetime = 10.0  # Disappears after 10 seconds
        self.time = 0
        self.bob_offset = 0

    def draw(self, screen):
        # Draw with bobbing animation
        bob_y = self.position.y + 5 * math.sin(self.bob_offset)
        
        if self.powerup_type == POWERUP_SHIELD:
            # Draw shield power-up (blue circle with inner ring)
            pygame.draw.circle(screen, (0, 100, 255), (int(self.position.x), int(bob_y)), self.radius, 3)
            pygame.draw.circle(screen, (100, 150, 255), (int(self.position.x), int(bob_y)), self.radius - 5, 2)
        elif self.powerup_type == POWERUP_SPEED:
            # Draw speed power-up (red triangle)
            points = [
                (self.position.x, bob_y - self.radius),
                (self.position.x - self.radius, bob_y + self.radius),
                (self.position.x + self.radius, bob_y + self.radius)
            ]
            pygame.draw.polygon(screen, (255, 50, 50), points, 3)

    def update(self, dt):
        self.time += dt
        self.bob_offset += dt * 3
        if self.time >= self.lifetime:
            self.kill()
        self.wrap_around_screen()

    @staticmethod
    def spawn_random():
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        powerup_type = random.choice([POWERUP_SHIELD, POWERUP_SPEED])
        return PowerUp(x, y, powerup_type)
