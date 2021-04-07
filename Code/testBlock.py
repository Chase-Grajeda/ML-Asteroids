# Class that creates a simple square for testing purposes 

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 50
HEIGHT = 50

class TestBlock(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(BLACK) 
        self.image.set_colorkey(BLACK) 

        pygame.draw.rect(self.image, WHITE, [0, 0, WIDTH, HEIGHT], 1)
        self.rect = self.image.get_rect()