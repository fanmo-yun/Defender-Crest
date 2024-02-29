import os
import pygame
import setting
from button import GameButton
from turret import Turret

class Level_1:
    def __init__(self) -> None:
        self.clicked = False
        self.create = False
        self.level_1_image = pygame.image.load(os.path.join("maps", "level1", "level1.png")).convert_alpha()
        self.buy_turret_button = GameButton((128, 128, 0), setting.WHITE, "Buy", (130, 35), (setting.SCREEN_WIDTH + 10, 30))
        self.cancel_turret_button = GameButton((220, 20, 60), setting.WHITE, "Cancel", (130, 35), (setting.SCREEN_WIDTH + 10, 70))
        self.upgrade_turret_button = GameButton((255, 140, 0), setting.WHITE, "Upgrade", (130, 35), (setting.SCREEN_WIDTH + 10, 110))
        self.camp_button = GameButton((255, 204, 0), setting.WHITE, "Go to Camp", (130, 35), (setting.SCREEN_WIDTH + 10, setting.SCREEN_HEIGHT - 60))
        self.turrets_group = pygame.sprite.Group()
        self.load_turret()
    
    def load_turret(self):
        self.turret_sprite_sheet_image = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Idle.png")).convert_alpha()
        self.subsurface_rect = pygame.Rect(0, 0, 48, 48)
        self.sprite_subsurface = self.turret_sprite_sheet_image.subsurface(self.subsurface_rect)
        self.sprite_subsurface_rect = self.sprite_subsurface.get_rect()
    
    def create_turret(self, screen: pygame.Surface):
        pos = pygame.mouse.get_pos()
        mouse_tile_x = pos[0] // setting.TILE_SIZE
        mouse_tile_y = pos[1] // setting.TILE_SIZE
        if pos[0] < setting.SCREEN_WIDTH and pos[1] < setting.SCREEN_HEIGHT and self.create:
            self.sprite_subsurface_rect.center = pos
            screen.blit(self.sprite_subsurface, self.sprite_subsurface_rect)
            if pygame.mouse.get_pressed()[2] == 1 and self.clicked == False:
                self.turrets_group.add(Turret((mouse_tile_x, mouse_tile_y)))
                self.clicked = True
                self.create = False
            if pygame.mouse.get_pressed()[2] == 0:
                self.clicked = False
    
    def draw(self, screen: pygame.Surface):
        if self.buy_turret_button.draw(screen):
            self.create = True

        self.cancel_turret_button.draw(screen)
        self.upgrade_turret_button.draw(screen)
        self.camp_button.draw(screen)

        screen.blit(self.level_1_image, (0, 0))
        self.turrets_group.update()
        self.turrets_group.draw(screen)

        self.create_turret(screen)
