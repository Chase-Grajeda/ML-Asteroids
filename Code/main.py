import numpy as np 
import pygame
import math 
import sys
from ship import *
from roid import *
from testBlock import * 

DISPLAY_W = 700
DISPLAY_H = 500
BORDER_BOX = (100, 100, 500, 300) 

def spawn_asteroid(asteroid_list): 
    
    side = np.random.randint(0, 4) # Left = 0, Right = 1, Top = 2, Bottom = 3
    #if side == 0: 
    #    xPos = np.random.randint(0, 101) 
    #    yPos = np.random.randint(0, 501) 
    #elif side == 1: 
    #    xPos = np.random.randint(600, 701) 
    #    yPos = np.random.randint(0, 501) 
    #elif side == 2: 
    #    xPos = np.random.randint(100, 601) 
    #    yPos = np.random.randint(0, 101) 
    #elif side == 3: 
    #    xPos = np.random.randint(100, 601) 
    #    yPos = np.random.randint(400, 501) 
    
    if side == 0: 
        xPos = 0
        yPos = np.random.randint(0, 501) 
    elif side == 1: 
        xPos = 700
        yPos = np.random.randint(0, 501) 
    elif side == 2: 
        xPos = np.random.randint(0, 701) 
        yPos = 0 
    elif side == 3: 
        xPos = np.random.randint(0, 701) 
        yPos = 500 

    speed = np.random.randint(1, 3)
    
    asteroid = Asteroid(xPos, yPos, speed) 
    asteroid_list.add(asteroid) 
    
    print("New asteroid") 
    


def run_game():
    # SETUP ----------------------------------
    # Initialize game space 
    pygame.init()

    # Set window size and caption
    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])
    pygame.display.set_caption("Test")
    
    playerShip = Ship()
    
    asteroid_list = pygame.sprite.Group() 
    

    # Run game
    running = True
    spawnBox = True # For testing 

    # Create game time, FPS
    clock = pygame.time.Clock()
    
    SPAWN_AST = pygame.USEREVENT 
    MOVE_AST = pygame.USEREVENT 
    
    pygame.time.set_timer(SPAWN_AST, 1000) # Trigger SPAWN_AST every 1s 

    # GAME LOOP ------------------------------
    while running:

        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                running = False
            if event.type == SPAWN_AST: 
                if len(asteroid_list) == 0: 
                    spawn_asteroid(asteroid_list) 

                
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]: 
            playerShip.rotate("right")
        if keys[pygame.K_RIGHT]:
            playerShip.rotate("left") 

        # UPDATES ----------------------------
        # Placements
        screen.fill((0, 0, 0))  # Black screen
        
        for ast in asteroid_list:
            # Move every asteroid +1 based on its trajectory  
            ast.move() 
            ast.killCheck() 

        # Update screen
        screen.blit(playerShip.getImg(), playerShip.getRect()) 
        for ast in asteroid_list: 
            newX, newY, xSize, ySize = ast.updateRect()
            screen.blit(ast.getImg(), ast.getRect())
        
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
