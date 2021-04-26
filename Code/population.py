import pygame 
import math 
import numpy as np 
from ship import * 
from roid import * 
from bullet import * 

class Population(): 
    def __init__(self): 
        
        super().__init__() 
        # Fitness 
        self.gameOver = False 
        self.score = 0 
        
        # Assets 
        self.playerShip = Ship() 
        self.ship_list = pygame.sprite.Group() 
        self.ship_list.add(self.playerShip) 
        
        self.asteroid_list = pygame.sprite.Group() 
        
        self.bullet_list = pygame.sprite.Group() 
        
    def getStatus(self): 
        return self.gameOver 
        
    def getShipImg(self): 
        return self.playerShip.getImg() 
    
    
    def getShipRect(self): 
        return self.playerShip.getRect() 
    
    def shipMove(self, direction): 
        if direction == 0: 
            self.playerShip.rotate("left") 
        if direction == 1: 
            self.playerShip.rotate("right") 
            
    def spawnAsteroid(self): 
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
        self.asteroid_list.add(asteroid) 
        
    def getAstList(self): 
        return self.asteroid_list
        
    