# Put asteroid class here

import pygame
import math 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 50
HEIGHT = 50
# Eventually HEIGHT and WIDTH will have to be variable upon class call 

xCenter = 700/2
yCenter = 500/2 

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos):

        super().__init__()
        self.xPos = xPos # Unused
        self.yPos = yPos # Unused 
        self.image = pygame.image.load("Assets/Asteroid_L.png")
        self.rect = self.image.get_rect(center=(xPos, yPos))
        
        self.radian = math.atan2(yCenter - yPos, xCenter - xPos) 
        # self.radian = math.atan2(1, 0) 
        self.dx = math.cos(self.radian) 
        self.dy = math.sin(self.radian) 

        # Remember, slope is y2-y1/x2-x1
        
    def getImg(self): 
        return self.image 
    
    def getRect(self): 
        return self.rect
    
    def move(self): 
        self.rect.x += self.dx 
        self.rect.y += self.dy 