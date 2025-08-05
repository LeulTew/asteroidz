import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

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
    # Instantiate player in the middle of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Instantiate asteroid field
    asteroid_field = AsteroidField()
    # Game loop
    while True:
        # 1. Check for player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # 2. Update the game world
        updatable.update(dt)
        # Collision check: player vs asteroids
        for asteroid in asteroids:
            if player.collide(asteroid):
                print("Game over!")
                pygame.quit()
                exit()
        # 3. Draw the game to the screen
        screen.fill((0, 0, 0))
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        dt = fpsClock.tick(60) / 1000.0  # Limit to 60 FPS and set delta time

if __name__ == "__main__":
    main()
