import os
import pygame
import setting
import json
from button import GameButton
from turret import Turret

class Level_1:
    def __init__(self) -> None:
        self.clicked = False
        self.create = False
        self.selected = False
        self.choose_turret = None
        self.level_1_image = pygame.image.load(os.path.join("maps", "level1", "level1.png")).convert_alpha()
        self.buy_turret_button = GameButton((128, 128, 0), setting.WHITE, "Buy", (130, 35), (setting.SCREEN_WIDTH + 10, 30))
        self.cancel_turret_button = GameButton((220, 20, 60), setting.WHITE, "Cancel", (130, 35), (setting.SCREEN_WIDTH + 10, 70))
        self.upgrade_turret_button = GameButton((255, 140, 0), setting.WHITE, "Upgrade", (130, 35), (setting.SCREEN_WIDTH + 10, 110))
        self.sell_turret_button = GameButton((211, 211, 211), setting.WHITE, "Sell", (130, 35), (setting.SCREEN_WIDTH + 10, 150))
        self.camp_button = GameButton((255, 204, 0), setting.WHITE, "Go to Camp", (130, 35), (setting.SCREEN_WIDTH + 10, setting.SCREEN_HEIGHT - 60))
        self.turrets_group = pygame.sprite.Group()
        self.load_turret()
        self.load_data()
    
    def load_data(self):
        with open(os.path.join("maps", "level1", "level1.json"), "r", encoding="UTF-8") as fp:
            data = fp.read()
        
        self.json_data = json.loads(data)
        self.tile_data = self.json_data["layers"][0]["data"]
        self.waypoints = self.json_data["layers"][1]["objects"][0]["polyline"]
    
    def load_turret(self):
        self.turret_sprite_sheet_image = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Idle.png")).convert_alpha()
        self.subsurface_rect = pygame.Rect(0, 0, 48, 48)
        self.sprite_subsurface = self.turret_sprite_sheet_image.subsurface(self.subsurface_rect)
        self.sprite_subsurface_rect = self.sprite_subsurface.get_rect()

    def selected_turret(self, pos):
        for t in self.turrets_group:
            if pos == (t.tile_x, t.tile_y):
                return t
        return None
    
    def check_turret(self, pos) -> bool:
        for t in self.turrets_group:
            if pos == (t.tile_x, t.tile_y):
                return False
        return True
    
    def reject_all(self):
        for t in self.turrets_group:
            t.selected = False
    
    def create_or_select_turret(self, screen: pygame.Surface):
        pos = pygame.mouse.get_pos()
        mouse_set_tile_x = pos[0] // setting.TILE_SIZE
        mouse_set_tile_y = pos[1] // setting.TILE_SIZE
        if pos[0] < setting.SCREEN_WIDTH and pos[1] < setting.SCREEN_HEIGHT and self.create:
            self.sprite_subsurface_rect.center = pos
            screen.blit(self.sprite_subsurface, self.sprite_subsurface_rect)
            if pygame.mouse.get_pressed()[2] == 1 and self.clicked == False:
                if self.check_turret((mouse_set_tile_x, mouse_set_tile_y)):
                    mouse_set_tile_num = (mouse_set_tile_y * setting.COLS) + mouse_set_tile_x
                    if self.tile_data[mouse_set_tile_num] == 38:
                        self.turrets_group.add(Turret((mouse_set_tile_x, mouse_set_tile_y)))
                        self.clicked = True
                        self.create = False
            if pygame.mouse.get_pressed()[2] == 0:
                self.clicked = False
        elif pos[0] < setting.SCREEN_WIDTH and pos[1] < setting.SCREEN_HEIGHT and self.create == False:
            if pygame.mouse.get_pressed()[2] == 1 and self.clicked == False:
                self.reject_all()
                self.choose_turret = self.selected_turret((mouse_set_tile_x, mouse_set_tile_y))
                if self.choose_turret != None:
                    self.choose_turret.selected = True
                    self.selected = True
                self.clicked = True
                self.create = False
            if pygame.mouse.get_pressed()[2] == 0:
                self.clicked = False
    
    def draw(self, screen: pygame.Surface):
        if self.buy_turret_button.draw(screen):
            if self.choose_turret != None:
                self.reject_all()
            self.create = True
            self.selected = False

        if self.selected:
            if self.cancel_turret_button.draw(screen):
                self.reject_all()
                self.selected = False
            self.upgrade_turret_button.draw(screen)
            if self.sell_turret_button.draw(screen):
                self.choose_turret.kill()
                self.selected = False
        self.camp_button.draw(screen)

        screen.blit(self.level_1_image, (0, 0))
        self.turrets_group.update()
        for turret in self.turrets_group:
            turret.draw(screen)

        self.create_or_select_turret(screen)
