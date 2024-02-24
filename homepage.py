import os
import sys
import pygame
import setting
from button import Button

class HomePage:
    def __init__(self) -> None:
        self.homepageimg = pygame.image.load(os.path.join("maps", "homepage", "homepage.png"))
        self.font = pygame.font.Font(os.path.join("font", "JetBrainsMono-Bold.ttf"), 52)
        self.text = self.font.render(setting.GAMETITLE, True, (64, 64, 64))
        self.buttons = pygame.sprite.Group()
        self.buttons.add(
            Button("#313336", "#D7FCD4", "start", (105, 35), (((setting.SCREEN_WIDTH + setting.BANNER_SIZE - 105)) / 2, 300)),
            Button("#313336", "#D7FCD4", "exit", (105, 35), (((setting.SCREEN_WIDTH + setting.BANNER_SIZE - 105)) / 2, 355)))
    
    def mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        if self.buttons.sprites()[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if mouse_click[0]:
                print("start")
        
        if self.buttons.sprites()[1].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if mouse_click[0]:
                sys.exit(0)
    
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.homepageimg, (0, 0))
        screen.blit(self.text, ((setting.SCREEN_WIDTH + setting.BANNER_SIZE - self.text.get_width()) / 2, 120))
        self.buttons.draw(screen)
        self.mouse_click()
        
