# Put asteroid class here

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 50
HEIGHT = 50
# Eventually HEIGHT and WIDTH will have to be variable upon class call 

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos):

        super().__init__()
        self.xPos = xPos
        self.yPos = yPos
        self.image = pygame.image.load("Assets/Asteroid_L.png")
        self.rect = self.image.get_rect(center=(self.xPos, self.yPos))
        
    def getImg(self): 
        return self.image 
    
    def getRect(self): 
        return self.rect