import pygame
import random
from circleshape import CircleShape
from constants import (PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, 
                     PLAYER_SHOOT_COOLDOWN, PLAYER_ACCELERATION, PLAYER_MAX_SPEED,
                     PLAYER_FRICTION, WEAPON_TYPE_NORMAL, WEAPON_TYPE_SHOTGUN, 
                     SHOTGUN_PELLET_COUNT, SHOTGUN_SPREAD_ANGLE)
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.weapon_type = WEAPON_TYPE_NORMAL

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    def shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            
            if self.weapon_type == WEAPON_TYPE_NORMAL:
                velocity = forward * PLAYER_SHOOT_SPEED
                Shot(self.position.x, self.position.y, velocity)
            elif self.weapon_type == WEAPON_TYPE_SHOTGUN:
                for i in range(SHOTGUN_PELLET_COUNT):
                    spread = random.uniform(-SHOTGUN_SPREAD_ANGLE, SHOTGUN_SPREAD_ANGLE)
                    velocity = forward.rotate(spread) * PLAYER_SHOOT_SPEED
                    Shot(self.position.x, self.position.y, velocity)

    def switch_weapon(self):
        if self.weapon_type == WEAPON_TYPE_NORMAL:
            self.weapon_type = WEAPON_TYPE_SHOTGUN
        else:
            self.weapon_type = WEAPON_TYPE_NORMAL
        print(f"Switched to weapon type: {self.weapon_type}")

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        
        is_accelerating = keys[pygame.K_w]
        if is_accelerating:
            self.move(dt)
        else:
            self.velocity *= PLAYER_FRICTION

        if keys[pygame.K_s]:
            self.velocity *= 0.9 # braking
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # This is a simple way to handle a single key press event for switching weapons
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_e:
                self.switch_weapon()
            pygame.event.post(event) # Post the event back to the queue

        if self.shoot_timer > 0:
            self.shoot_timer -= dt
        self.position += self.velocity * dt
        self.wrap_around_screen()

