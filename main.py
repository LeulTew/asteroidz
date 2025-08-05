import pygame
from constants import *
from player import Player

def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fpsClock = pygame.time.Clock()
    dt = 0
    # Instantiate player in the middle of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Game loop
    while True:
        # 1. Check for player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # 2. Update the game world
        # (No game world updates yet)
        # 3. Draw the game to the screen
        screen.fill((0, 0, 0))
        player.update(dt)
        player.draw(screen)
        pygame.display.flip()
        dt = fpsClock.tick(60) / 1000.0  # Limit to 60 FPS and set delta time

if __name__ == "__main__":
    main()
