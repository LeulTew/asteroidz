import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from background import draw_background
from powerup import PowerUp, POWERUP_SHIELD, POWERUP_SPEED
from bomb import Bomb
from particles import ParticleSystem
import random

# Global particle system
particle_system = None

def main():
    global particle_system
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fpsClock = pygame.time.Clock()
    dt = 0
    
    # Initialize particle system
    particle_system = ParticleSystem()
    # Create groups for updatable and drawable objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    # Set containers for Player, Asteroid, AsteroidField, Shot, Explosion, PowerUp, and Bomb
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)
    # Instantiate player in the middle of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Instantiate asteroid field
    asteroid_field = AsteroidField()
    score = 0
    lives = PLAYER_LIVES
    font = pygame.font.Font(None, 36)
    powerup_timer = 0
    # Game loop
    while True:
        # 1. Check for player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # 2. Update the game world
        updatable.update(dt)
        
        # Spawn power-ups occasionally
        powerup_timer += dt
        if powerup_timer > 15:  # Spawn every 15 seconds
            PowerUp.spawn_random()
            powerup_timer = 0
        
        # Collision check: player vs asteroids
        for asteroid in list(asteroids):
            if player.collide(asteroid) and not player.is_shielded():
                lives -= 1
                if lives <= 0:
                    print("Game over!")
                    pygame.quit()
                    exit()
                else:
                    player.kill()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # Collision check: player vs power-ups
        for powerup in list(powerups):
            if player.collide(powerup):
                if powerup.powerup_type == POWERUP_SHIELD:
                    player.activate_shield()
                elif powerup.powerup_type == POWERUP_SPEED:
                    player.activate_speed_boost()
                powerup.kill()
                
        # Collision check: bullets vs asteroids
        for asteroid in list(asteroids):
            for shot in list(shots):
                if shot.collide(asteroid):
                    score += asteroid.split()
                    shot.kill()
        
        # Collision check: bombs vs asteroids (when bombs explode)
        for bomb in list(bombs):
            if bomb.exploded:
                bomb_pos = bomb.position
                for asteroid in list(asteroids):
                    distance = bomb_pos.distance_to(asteroid.position)
                    if distance < 100:  # Bomb blast radius
                        score += asteroid.split()
        
        # 3. Draw the game to the screen
        draw_background(screen)
        for obj in drawable:
            obj.draw(screen)
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        # Draw lives
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
        # Draw weapon type
        weapon_text = font.render(f"Weapon: {'Normal' if player.weapon_type == WEAPON_TYPE_NORMAL else 'Shotgun'}", True, (255, 255, 255))
        screen.blit(weapon_text, (10, 50))
        # Draw bombs remaining
        bombs_text = font.render(f"Bombs: {player.bombs}", True, (255, 255, 255))
        screen.blit(bombs_text, (10, 90))
        # Draw power-up status
        if player.shield_active:
            shield_text = font.render(f"Shield: {player.shield_timer:.1f}s", True, (0, 150, 255))
            screen.blit(shield_text, (10, 130))
        if player.speed_boost_active:
            speed_text = font.render(f"Speed Boost: {player.speed_boost_timer:.1f}s", True, (255, 200, 100))
            screen.blit(speed_text, (10, 170))
        
        pygame.display.flip()
        dt = fpsClock.tick(60) / 1000.0  # Limit to 60 FPS and set delta time

if __name__ == "__main__":
    main()
