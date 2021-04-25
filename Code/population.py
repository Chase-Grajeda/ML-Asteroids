import pygame 
import math 
import numpy as np 
from ship import * 
from roid import * 
from bullet import * 

class Population(): 
    def __init__(self): 
        
        super().__init__() 
        self.gameOver = False 
        
        self.playerShip = Ship() 
        self.ship_list = pygame.sprite.Group() 
        self.ship_list.add(self.playerShip) 
        self.asteroid_list = pygame.sprite.Group() 
        self.bullet_list = pygame.sprite.Group() 
        