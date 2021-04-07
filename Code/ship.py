# Put ship class here
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 16
HEIGHT = 20
TRI_DIM = [[0, 0], [WIDTH/2, HEIGHT], [WIDTH, 0] ] #(x, y) 

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        # self.ship = pygame.draw.rect(screen, WHITE, [150, 10, 50, 20], 2)
        # self.ship = pygame.draw.polygon(screen, WHITE, [[10, 10], [0, 200], [200, 200]], 3)

        super().__init__()
        
        self.image = pygame.image.load("Assets/Ship.png")
        self.rect = self.image.get_rect() 

    def move_left(self): 
        self.rect.x -= 5 