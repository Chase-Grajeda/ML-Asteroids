# Put asteroid class here

import pygame
import math 
import numpy as np 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 50
HEIGHT = 50
# Eventually HEIGHT and WIDTH will have to be variable upon class call 

xCenter = 700/2
yCenter = 500/2 

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, speed):

        super().__init__()
        self.xPos = xPos 
        self.yPos = yPos 
        self.speed = speed 
        self.image = pygame.image.load("Assets/Asteroid_L.png")
        self.rect = self.image.get_rect(center=(xPos, yPos))
        
        self.radian = math.atan2(yCenter - yPos, xCenter - xPos) 
        self.radian += np.random.uniform(-0.3, 0.3) # Gives a bit of randomness to the paths
        self.dx = math.cos(self.radian) 
        self.dy = math.sin(self.radian) 
        
    def getImg(self): 
        return self.image 
    
    def getRect(self): 
        return self.rect
    
    def move(self): 
        self.xPos += self.dx * self.speed 
        self.yPos += self.dy * self.speed 
        self.rect.center = (self.xPos, self.yPos) 
        
    def updateRect(self): 
        return self.xPos, self.yPos, WIDTH, HEIGHT
        
    def killCheck(self): 
        if self.xPos >= 700 + 50 or self.xPos <= 0 - 50 or \
            self.yPos >= 500 + 50 or self.yPos <= 0 - 50: 
            
            self.kill() 
            print("Killed asteroid") 
            return 
        
        else: 
            return 
            
    def destroy(self): 
        self.kill() 
        print("Killed asteroid")