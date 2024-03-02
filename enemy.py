import os
import pygame
import setting

def load_enemy_sprite_sheets(enemy_type) -> list[pygame.Surface]:
    sprite_sheets = list()
    
    for state in setting.ENEMY_STATE:
        if enemy_type == "Slime":
            sprite_sheets.append(pygame.image.load(os.path.join("assets", "enemies", "1", f"D_{state}.png")).convert_alpha())
        elif enemy_type == "goblin":
            sprite_sheets.append(pygame.image.load(os.path.join("assets", "enemies", "2", f"D_{state}.png")).convert_alpha())
        elif enemy_type == "wolf":
            sprite_sheets.append(pygame.image.load(os.path.join("assets", "enemies", "3", f"D_{state}.png")).convert_alpha())
        else:
            sprite_sheets.append(pygame.image.load(os.path.join("assets", "enemies", "4", f"D_{state}.png")).convert_alpha())
    
    return sprite_sheets
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self, rank_num, waypoints, pos) -> None:
        super().__init__()
        self.waypoints = waypoints
        self.rank_num = rank_num
        self.pos = pos

class Slime(Enemy):
    def __init__(self, rank_num, waypoints, pos) -> None:
        super().__init__(rank_num, waypoints, pos)
        self.sprite_sheets = load_enemy_sprite_sheets(self.__class__.__name__)
        self.process_sheets()
        
        self.image = self.walk_sprite_sheet_images[0]
        self.rect = self.image.get_rect()
    
    def process_sheets(self):
        self.walk_sprite_sheet_images = list()
        self.death_sprite_sheet_images = list()
        for i in range(6):
            self.walk_sprite_sheet_images.append(self.sprite_sheets[0].subsurface(i * setting.ENEMY_SIZE, 0, setting.ENEMY_SIZE, setting.ENEMY_SIZE))
            self.death_sprite_sheet_images.append(self.sprite_sheets[1].subsurface(i * setting.ENEMY_SIZE, 0, setting.ENEMY_SIZE, setting.ENEMY_SIZE))

class goblin(Enemy):
    def __init__(self, rank_num, waypoints, pos) -> None:
        super().__init__(rank_num, waypoints, pos)
        self.sprite_sheets = load_enemy_sprite_sheets(self.__class__.__name__)

class wolf(Enemy):
    def __init__(self, rank_num, waypoints, pos) -> None:
        super().__init__(rank_num, waypoints, pos)
        self.sprite_sheets = load_enemy_sprite_sheets(self.__class__.__name__)

class Bee(Enemy):
    def __init__(self, rank_num, waypoints, pos) -> None:
        super().__init__(rank_num, waypoints, pos)
        self.sprite_sheets = load_enemy_sprite_sheets(self.__class__.__name__)
