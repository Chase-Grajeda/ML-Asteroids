import numpy as np 
import pygame
import sys
from ship import *
from roid import *
from testBlock import * 

DISPLAY_W = 700
DISPLAY_H = 500
BORDER_BOX = (100, 100, 500, 300) 

def spawn_asteroid(asteroid_list): 
    
    xPos = np.random.randint(1, 701) 
    yPos = np.random.randint(1, 501) 
    asteroid = Asteroid(xPos, yPos) 
    asteroid_list.append(asteroid) 
    
    print("New asteroid") 
    


def run_game():
    # SETUP ----------------------------------
    # Initialize game space 
    pygame.init()

    # Set window size and caption
    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])
    pygame.display.set_caption("Test")

    
    
    playerShip = Ship()
    asteroid = Asteroid(700/3, 500/3) 
    asteroid_list = [asteroid]

    # Run game
    running = True
    spawnBox = True # For testing 

    # Create game time, FPS
    clock = pygame.time.Clock()
    
    SPAWN_AST = pygame.USEREVENT 
    pygame.time.set_timer(SPAWN_AST, 1000) # Trigger SPAWN_AST every 1s 

    # GAME LOOP ------------------------------
    while running:

        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                running = False
            if event.type == SPAWN_AST: 
                spawn_asteroid(asteroid_list) 
                
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
        for ast in asteroid_list: 
            screen.blit(ast.getImg(), ast.getRect())
        
        # screen.blit(asteroid.getImg(), asteroid.getRect())
        
        # Testing 
        if spawnBox == True: 
            pygame.draw.rect(screen, WHITE, BORDER_BOX, 2) 
        
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
