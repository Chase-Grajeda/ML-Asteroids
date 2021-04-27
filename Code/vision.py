import pygame 
import math 

class Vision(pygame.sprite.Sprite): 
    def __init__(self, surface, angle): 
        
        super().__init__() 
        self.image = pygame.image.load("Assets/V-line.png") 
        self.rot_image = pygame.transform.rotozoom(self.image, angle, 1)
        self.rot_rect = self.rot_image.get_rect() 
        if(angle == 0): 
            self.rot_rect = self.rot_image.get_rect(midbottom=(700/2,500/2))
        if(angle == 45): 
            self.rot_rect = self.rot_image.get_rect(bottomright=(700/2, 500/2))
        if(angle == 90): 
            self.rot_rect = self.rot_image.get_rect(midright=(700/2, 500/2))
        if(angle == 135): 
            self.rot_rect = self.rot_image.get_rect(topright=(700/2, 500/2))
        if(angle == 180): 
            self.rot_rect = self.rot_image.get_rect(midtop=(700/2, 500/2))
        if(angle == 225): 
            self.rot_rect = self.rot_image.get_rect(topleft=(700/2, 500/2))
        if(angle == 270): 
            self.rot_rect = self.rot_image.get_rect(midleft=(700/2, 500/2))
        if(angle == 315): 
            self.rot_rect = self.rot_image.get_rect(bottomleft=(700/2, 500/2))
        
        self.rect = self.rot_rect 
        
    def getImg(self): 
        return self.rot_image 
    
    def getRect(self): 
        return self.rot_rect  
        
        