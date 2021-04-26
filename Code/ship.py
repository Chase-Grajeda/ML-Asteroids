# Put ship class here
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 16
HEIGHT = 20

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        
        super().__init__()
        
        self.image = pygame.image.load("Assets/Ship.png")
        self.rect = self.image.get_rect(center=(700/2, 500/2)) 
        self.tempImage = self.image 
        self.tempRect = self.rect 
        self.angle = 0
    
    def rot(self, surface, angle): 
        rot_image = pygame.transform.rotozoom(surface, angle*-1, 1) 
        rot_rect = rot_image.get_rect(center=(700/2, 500/2)) 
        
        return rot_image, rot_rect 
        
    
    def rotate(self, direction): 
        if(direction == "right"): 
            self.angle += 5
        if(direction == "left"): 
            self.angle -= 5 
            
        self.tempImage, self.tempRect = self.rot(self.image, self.angle)

    
    def getImg(self): 
        return self.tempImage 
    
    
    def getRect(self): 
        return self.tempRect 
    
    def getAngle(self): 
        return self.angle 
    
    def getORect(self): 
        return self.rect 
    
    def destroy(self): 
        self.kill() 