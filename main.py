import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from background import draw_background

def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fpsClock = pygame.time.Clock()
    dt = 0
    # Create groups for updatable and drawable objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    # Set containers for Player, Asteroid, AsteroidField, and Shot
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    # Instantiate player in the middle of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Instantiate asteroid field
    asteroid_field = AsteroidField()
    score = 0
    lives = PLAYER_LIVES
    font = pygame.font.Font(None, 36)
    # Game loop
    while True:
        # 1. Check for player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # 2. Update the game world
        updatable.update(dt)
        # Collision check: player vs asteroids
        for asteroid in list(asteroids):
            if player.collide(asteroid):
                lives -= 1
                if lives <= 0:
                    print("Game over!")
                    pygame.quit()
                    exit()
                else:
                    player.kill()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        # Collision check: bullets vs asteroids
        for asteroid in list(asteroids):
            for shot in list(shots):
                if shot.collide(asteroid):
                    score += asteroid.split()
                    shot.kill()
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
        pygame.display.flip()
        dt = fpsClock.tick(60) / 1000.0  # Limit to 60 FPS and set delta time

if __name__ == "__main__":
    main()
