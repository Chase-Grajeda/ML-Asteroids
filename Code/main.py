import numpy
import pygame
import sys
from ship import *
from roid import *
from testBlock import * 

DISPLAY_W = 700
DISPLAY_H = 500


def run_game():
    # SETUP ----------------------------------
    # Initialize game space
    pygame.init()

    # Set window size and caption
    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])
    pygame.display.set_caption("Test")

    playerShip = Ship()
    asteroid = Asteroid() 

    # Run game
    running = True

    # Create game time, FPS
    clock = pygame.time.Clock()

    # GAME LOOP ------------------------------
    while running:

        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                running = False
                
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]: 
            playerShip.rotate("right")
        if keys[pygame.K_RIGHT]:
            playerShip.rotate("left") 

        # UPDATES ----------------------------
        # Placements
        screen.fill((0, 0, 0))  # Black screen

        # Update screen
        screen.blit(playerShip.getImg(), playerShip.getRect()) 
        screen.blit(asteroid.getImg(), asteroid.getRect())
        
        pygame.display.flip()
        clock.tick(60)

    # EXIT HANDLING 
    pygame.display.quit()
    pygame.quit()
    # sys.quit()


if __name__ == "__main__":
    print("Running game")
    run_game()
    print("Game closed")
