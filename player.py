import pygame
import random
from circleshape import CircleShape
from constants import (PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, 
                     PLAYER_SHOOT_COOLDOWN, PLAYER_ACCELERATION, PLAYER_MAX_SPEED,
                     PLAYER_FRICTION, WEAPON_TYPE_NORMAL, WEAPON_TYPE_SHOTGUN, 
                     SHOTGUN_PELLET_COUNT, SHOTGUN_SPREAD_ANGLE)
from shot import Shot
from bomb import Bomb

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.weapon_type = WEAPON_TYPE_NORMAL
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.bombs = 3  # Player starts with 3 bombs

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Draw shield effect if active
        if self.shield_active:
            pygame.draw.circle(screen, (0, 150, 255), self.position, self.radius + 10, 3)
        
        # Draw player triangle with speed boost effect
        color = (255, 255, 255)
        if self.speed_boost_active:
            color = (255, 200, 100)  # Yellow tint when speed boosted
            
        pygame.draw.polygon(screen, color, self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        acceleration = PLAYER_ACCELERATION
        max_speed = PLAYER_MAX_SPEED
        
        # Apply speed boost if active
        if self.speed_boost_active:
            acceleration *= 1.5
            max_speed *= 1.5
            
        self.velocity += forward * acceleration * dt
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

    def activate_shield(self, duration=5.0):
        self.shield_active = True
        self.shield_timer = duration

    def activate_speed_boost(self, duration=5.0):
        self.speed_boost_active = True
        self.speed_boost_timer = duration

    def drop_bomb(self):
        if self.bombs > 0:
            bomb = Bomb(self.position.x, self.position.y)
            bomb.velocity = self.velocity * 0.5  # Inherit some player velocity
            self.bombs -= 1
            return bomb
        return None

    def is_shielded(self):
        return self.shield_active

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

    def collide(self, other):
        # Override collision to use triangular hitbox
        triangle_points = self.triangle()
        
        # Simple collision detection using distance to triangle center
        # For more accurate collision, we'd need point-in-polygon testing
        center = pygame.Vector2(0, 0)
        for point in triangle_points:
            center += point
        center /= len(triangle_points)
        
        distance = center.distance_to(other.position)
        return distance <= (self.radius * 0.8 + other.radius)  # Slightly smaller hitbox

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
        if keys[pygame.K_b]:
            self.drop_bomb()
        
        # This is a simple way to handle a single key press event for switching weapons
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_e:
                self.switch_weapon()
            pygame.event.post(event) # Post the event back to the queue

        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            
        # Update power-up timers
        if self.shield_timer > 0:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False
                
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
                
        self.position += self.velocity * dt
        self.wrap_around_screen()

