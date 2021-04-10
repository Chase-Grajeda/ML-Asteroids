import pygame 
import math 

WIDTH = 2
HEIGHT = 5 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos): 
        
        super().__init__() 
        self.xPos = xPos 
        self.yPos = yPos 
        self.image = pygame.image.load("Assets/Bullet.png")
        self.rect = self.image.get_rect(center=(xPos, yPos))
    
    
    def move(self): 
        self.yPos -= 5
        self.rect.center = (self.xPos, self.yPos) 
    
    def getImg(self): 
        return self.image 
    
    def getRect(self): 
        return self.rect 
    
    def killCheck(self): 
        if self.yPos >= 500 + 5 or self.yPos <= 0 - 5: 
            self.kill() 
            print("Bullet destroyed") 
            return 

        else: 
            return 