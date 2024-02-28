import os
import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, color, text_color, text, size, pos) -> None:
        super().__init__()
        self.color = color
        self.font = pygame.font.Font(os.path.join("font", "JetBrainsMono-Bold.ttf"), 20)
        self.f = self.font.render(text, True, text_color)
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.image.blit(self.f, self.f.get_rect(center=(size[0]/2, size[1]/2)))
        self.rect = self.image.get_rect(topleft=pos)

class GameButton():
    def __init__(self, color, text_color, text, size, pos) -> None:
        self.clicked = False
        self.font = pygame.font.Font(os.path.join("font", "JetBrainsMono-Bold.ttf"), 20)
        self.f = self.font.render(text, True, text_color)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.image.blit(self.f, self.f.get_rect(center=(size[0]/2, size[1]/2)))
        self.rect = self.image.get_rect(topleft=pos)
    
    def draw(self, screen: pygame.Surface):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
        return action