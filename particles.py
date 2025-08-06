import pygame
import random
import math

class Particle:
    def __init__(self, x, y, velocity, color, lifetime):
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.color = color
        self.lifetime = lifetime
        self.time = 0
        self.size = random.uniform(1, 3)

    def update(self, dt):
        self.time += dt
        self.position += self.velocity * dt
        return self.time < self.lifetime

    def draw(self, screen):
        alpha = 1 - (self.time / self.lifetime)
        current_size = int(self.size * alpha)
        if current_size > 0:
            pygame.draw.circle(screen, self.color, self.position, current_size)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_explosion(self, position, count=20):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            color = random.choice([(255, 100, 0), (255, 200, 0), (255, 255, 100)])
            self.particles.append(Particle(position.x, position.y, velocity, color, random.uniform(0.5, 1.5)))

    def add_thrust(self, position, direction):
        # Add thrust particles behind the ship
        for _ in range(3):
            angle = direction + random.uniform(-0.3, 0.3)
            speed = random.uniform(100, 200)
            velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            color = (100, 150, 255)
            self.particles.append(Particle(position.x, position.y, velocity, color, 0.3))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
