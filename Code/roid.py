# Put asteroid class here

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 30
HEIGHT = 30

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        # self.ship = pygame.draw.rect(screen, WHITE, [150, 10, 50, 20], 2)
        # self.ship = pygame.draw.polygon(screen, WHITE, [[10, 10], [0, 200], [200, 200]], 3)

        super().__init__()
        
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(BLACK) 
        self.image.set_colorkey(BLACK) 

        pygame.draw.rect(self.image, WHITE, [0, 0, WIDTH, HEIGHT], 1)
        self.rect = self.image.get_rect()