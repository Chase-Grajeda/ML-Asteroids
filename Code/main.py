import numpy
import pygame
import sys
from ship import *
from roid import *
from testBlock import * 

DISPLAY_W = 700
DISPLAY_H = 500


def run_game():
    # Initialize game space
    pygame.init()

    # Set window size and caption
    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])
    pygame.display.set_caption("Test")

    # Sprite container
    sprite_list = pygame.sprite.Group()

    playerShip = Ship()
    playerShip.rect.x = DISPLAY_W/2 
    playerShip.rect.y = DISPLAY_H/2
    
    asteroid = Asteroid() 
    asteroid.rect.x = DISPLAY_W/3 
    asteroid.rect.y = DISPLAY_H/3

    sprite_list.add(playerShip)
    sprite_list.add(asteroid) 

    # Run game
    running = True

    # Create game time, FPS
    clock = pygame.time.Clock()

    # TO EXIT, PRESS SPACE BAR
    while running:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                if event.key == pygame.K_LEFT:
                    playerShip.move_left() 
                    
            if event.type == pygame.QUIT:
                running = False

        # Placements
        screen.fill((0, 0, 0))  # Black screen

        # Update sprites
        sprite_list.update()
        sprite_list.draw(screen)

        # Update screen
        pygame.display.flip()

        # Limit to 60 FPS
        clock.tick(60)

    pygame.display.quit()
    pygame.quit()
    # sys.quit()


if __name__ == "__main__":
    print("Running game")
    run_game()
    print("Game closed")
