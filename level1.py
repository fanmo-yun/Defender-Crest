import os
import pygame

class Level_1:
    def __init__(self) -> None:
        self.level_1_image = pygame.image.load(os.path.join("maps", "level1", "level1.png")).convert_alpha()
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.level_1_image, (0, 0))