import numpy as np 
import pygame
import math 
import sys
from ship import *
from roid import *
from bullet import * 
from testBlock import * 

DISPLAY_W = 700
DISPLAY_H = 500
BORDER_BOX = (100, 100, 500, 300) 
AST_LIMIT = 5

def spawn_asteroid(asteroid_list): 
    
    side = np.random.randint(0, 4) # Left = 0, Right = 1, Top = 2, Bottom = 3
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
    

def fire(bullet_list, playerShip): 
    
    center = playerShip.getORect().center 
    top = (playerShip.getORect()).top
    
    radius = center[1] - top 
    
    posX = center[0]
    posY = center[1]
    
    angle = playerShip.getAngle() 
    
    # Trig is weird because of how pygame percieves the grid space 
    dx = radius * math.sin(math.radians(angle)) 
    dy = radius * math.cos(math.radians(angle)) 
    
    posX += dx  
    posY -= dy 
    
    bullet = Bullet(posX, posY, angle) 
    bullet_list.add(bullet) 
    
    # None of the above works, finds the incorrect circle 
    



def run_game():
    # SETUP ----------------------------------
    # Initialize game space 
    pygame.init()

    # Set window size and caption
    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])
    pygame.display.set_caption("Test")
    
    playerShip = Ship()
    
    asteroid_list = pygame.sprite.Group() 
    bullet_list = pygame.sprite.Group() 
    
    

    # Run game
    running = True
    spawnBox = False # For testing 

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
                if len(asteroid_list) < AST_LIMIT: 
                    spawn_asteroid(asteroid_list) 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE: 
                    fire(bullet_list, playerShip) 

                
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]: 
            playerShip.rotate("left")
        if keys[pygame.K_RIGHT]:
            playerShip.rotate("right") 

        # UPDATES ----------------------------
        # Placements
        screen.fill((0, 0, 0))  # Black screen
        
        # Move asteroids based on their trajectories 
        for ast in asteroid_list:
            ast.move() 
            ast.killCheck() 
        for blt in bullet_list: 
            blt.move() 
            blt.killCheck() 
            
        # Check to see if any asteroids have collided with the player 
        collision = pygame.sprite.spritecollide(playerShip, asteroid_list, False) 
        for ast in collision: 
            ast.destroy() 

        # Check to see if any bullets have collided with an asteroid 
        for blt in bullet_list: 
            bullet_x_ast = pygame.sprite.spritecollide(blt, asteroid_list, False) 
            for ast in bullet_x_ast: 
                print("Collision") 
                ast.destroy() 
                blt.destroy() 
        
        
        # Update screen
        screen.blit(playerShip.getImg(), playerShip.getRect()) 
        for ast in asteroid_list: 
            newX, newY, xSize, ySize = ast.updateRect()
            screen.blit(ast.getImg(), ast.getRect())
        for blt in bullet_list: 
            screen.blit(blt.getImg(), blt.getRect())
        
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
