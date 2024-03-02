import os
import pygame
import setting
from turret_rank import RANK

class Turret(pygame.sprite.Sprite):
    def load_images(self) -> None:
        self.idle_sprite_sheet_images_1 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Idle.png")).convert_alpha()
        self.attack_sprite_sheet_images_1 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Attack.png")).convert_alpha()
        
        self.idle_sprite_sheet_images_2 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "2", "D_Idle.png")).convert_alpha()
        self.attack_sprite_sheet_images_2 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "2", "D_Attack.png")).convert_alpha()
        
        self.idle_sprite_sheet_images_3 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "3", "D_Idle.png")).convert_alpha()
        self.attack_sprite_sheet_images_3 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "3", "D_Attack.png")).convert_alpha()
        
        self.idle_sprite_images_1 = list()
        self.attack_sprite_images_1 = list()
        
        self.idle_sprite_images_2 = list()
        self.attack_sprite_images_2 = list()
        
        self.idle_sprite_images_3 = list()
        self.attack_sprite_images_3 = list()
        
        for idle_image in range(4):
            temp_image1 = self.idle_sprite_sheet_images_1.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE)
            temp_image2 = self.idle_sprite_sheet_images_2.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE)
            temp_image3 = self.idle_sprite_sheet_images_3.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE)
            
            self.idle_sprite_images_1.append(temp_image1)
            self.idle_sprite_images_2.append(temp_image2)
            self.idle_sprite_images_3.append(temp_image3)
            
        for attack_image in range(6):
            temp_image1 = self.attack_sprite_sheet_images_1.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE)
            temp_image2 = self.attack_sprite_sheet_images_2.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE)
            temp_image3 = self.attack_sprite_sheet_images_3.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE)
            
            self.attack_sprite_images_1.append(temp_image1)
            self.attack_sprite_images_2.append(temp_image2)
            self.attack_sprite_images_3.append(temp_image3)

    def __init__(self, pos) -> None:
        super().__init__()
        self.load_images()
        self.animation_index = 0
        self.animation_speed = 0.07
        self.selected = False
        self.tile_x = pos[0]
        self.tile_y = pos[1]
        self.x = (pos[0] + 0.5) * setting.TILE_SIZE
        self.y = (pos[1] + 0.5) * setting.TILE_SIZE
        
        self.image = self.idle_sprite_images_1[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.range_image = pygame.Surface((180, 180))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, (255, 255, 255), (90, 90), 90)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
    
    def play_animation(self) -> None:
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.idle_sprite_images_1):
            self.animation_index = 0
        self.image = self.idle_sprite_images_1[int(self.animation_index)]
    
    def update(self) -> None:
        self.play_animation()
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        if self.selected:
            screen.blit(self.range_image, self.range_rect)