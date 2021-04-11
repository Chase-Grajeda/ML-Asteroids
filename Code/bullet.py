import pygame 
import math 

WIDTH = 2
HEIGHT = 5 

xCenter = 700/2
yCenter = 500/2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, angle): 
        
        super().__init__() 
        self.xPos = xPos 
        self.yPos = yPos 
        self.speed = 5
        self.image = pygame.image.load("Assets/Bullet.png")
        self.rect = self.image.get_rect(center=(xPos, yPos))
        self.angle = angle * (-1)   # angle
        
        self.tempImage = pygame.transform.rotozoom(self.image, self.angle, 1)
        self.tempRect = self.tempImage.get_rect(center=(self.xPos, self.yPos)) 
        
        self.radian = math.atan2(yPos - yCenter, xPos - xCenter) 
        self.dx = math.cos(self.radian) 
        self.dy = math.sin(self.radian) 
        
    
    def move(self): 
        self.xPos += self.dx * self.speed 
        self.yPos += self.dy * self.speed  
        self.tempRect.center = (self.xPos, self.yPos) 
        self.rect.center = (self.xPos, self.yPos) 
    
    def getImg(self): 
        return self.tempImage 
    
    def getRect(self): 
        return self.tempRect
    
    def getORect(self): 
        return self.tempRect 
    
    def killCheck(self): 
        if self.yPos >= 500 + 5 or self.yPos <= 0 - 5: 
            self.kill()  
            return 

        else: 
            return 
        
    def destroy(self): 
        self.kill()