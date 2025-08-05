import pygame
from constants import *

def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        pygame.display.flip()

if __name__ == "__main__":
    main()
