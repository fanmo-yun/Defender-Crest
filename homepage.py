import os
import sys
import pygame
import setting
from button import Button
from levels import Level_1, Level_2, Level_3, Level_end

class HomePage:
    def __init__(self) -> None:
        self.start_game = False
        self.homepageimg = pygame.image.load(os.path.join("maps", "homepage", "homepage.png"))
        self.font = pygame.font.Font(os.path.join("font", "JetBrainsMono-Bold.ttf"), 52)
        self.text = self.font.render(setting.GAMETITLE, True, (64, 64, 64))
        self.buttons = pygame.sprite.Group()
        self.buttons.add(
            Button("#313336", "#D7FCD4", "start", (105, 35), (((setting.SCREEN_WIDTH + setting.BANNER_SIZE - 105)) / 2, 300)),
            Button("#313336", "#D7FCD4", "exit", (105, 35), (((setting.SCREEN_WIDTH + setting.BANNER_SIZE - 105)) / 2, 355)))
        self.level1 = Level_1()
        self.level2 = Level_2()
        self.level3 = Level_3()
        self.end = Level_end()
    
    def mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        if self.buttons.sprites()[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if mouse_click[0]:
                self.start_game = True
        
        if self.buttons.sprites()[1].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if mouse_click[0]:
                sys.exit(0)
    
    
    def draw(self, screen: pygame.Surface):
        if self.start_game == False:
            screen.blit(self.homepageimg, (0, 0))
            screen.blit(self.text, ((setting.SCREEN_WIDTH + setting.BANNER_SIZE - self.text.get_width()) / 2, 120))
            self.buttons.draw(screen)
            self.mouse_click()
        else:
            # if self.level1.is_pass_game == False:
            #     self.level1.draw(screen)
            # elif self.level2.is_pass_game == False:
            #     self.level2.draw(screen)
            # elif self.level3.is_pass_game == False:
            #     self.level3.draw(screen)
            # else:
            self.end.draw(screen, (self.level1.score, self.level2.score, self.level3.score))
