import math
import os
import pygame
import setting
from turret_rank import RANK

class Turret(pygame.sprite.Sprite):
    def load_images(self) -> None:
        self.idle_sprite_images_1 = list()
        self.attack_sprite_images_1 = list()
        
        self.idle_sprite_images_2 = list()
        self.attack_sprite_images_2 = list()
        
        self.idle_sprite_images_3 = list()
        self.attack_sprite_images_3 = list()
        
        self.idle_sprite_sheet_images_1 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Idle.png")).convert_alpha()
        self.attack_sprite_sheet_images_1 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Attack.png")).convert_alpha()
        
        self.idle_sprite_sheet_images_2 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "2", "D_Idle.png")).convert_alpha()
        self.attack_sprite_sheet_images_2 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "2", "D_Attack.png")).convert_alpha()
        
        self.idle_sprite_sheet_images_3 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "3", "D_Idle.png")).convert_alpha()
        self.attack_sprite_sheet_images_3 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "3", "D_Attack.png")).convert_alpha()
        
        
        for idle_image in range(4):
            self.idle_sprite_images_1.append(self.idle_sprite_sheet_images_1.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.idle_sprite_images_2.append(self.idle_sprite_sheet_images_2.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.idle_sprite_images_3.append(self.idle_sprite_sheet_images_3.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            
        for attack_image in range(6):
            self.attack_sprite_images_1.append(self.attack_sprite_sheet_images_1.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.attack_sprite_images_2.append(self.attack_sprite_sheet_images_2.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.attack_sprite_images_3.append(self.attack_sprite_sheet_images_3.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))

    def __init__(self, pos) -> None:
        super().__init__()
        self.load_images()
        self.selected = False
        self.rank = 1
        self.angle = 90
        self.tile_x = pos[0]
        self.tile_y = pos[1]
        self.animation_index = 0
        self.animation_speed = 0.07
        self.create_rank()
        self.x = (pos[0] + 0.5) * setting.TILE_SIZE
        self.y = (pos[1] + 0.5) * setting.TILE_SIZE
        
        self.image = self.idle_sprite_images_1[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.create_range()
    
    def create_rank(self) -> None:
        self.cost = RANK[self.rank - 1].get("cost")
        self.sell = RANK[self.rank - 1].get("sell")
        self.injure = RANK[self.rank - 1].get("injure")
        self.circle_range = RANK[self.rank - 1].get("range")
        self.cooldown = RANK[self.rank - 1].get("cooldown")
        self.hurt = RANK[self.rank - 1].get("hurt")
    
    def create_range(self) -> None:    
        self.range_image = pygame.Surface((self.circle_range * 2, self.circle_range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, (255, 255, 255), (self.circle_range, self.circle_range), self.circle_range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
    
    def play_animation(self) -> None:
        if self.rank == 1:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.idle_sprite_images_1):
                self.animation_index = 0
            self.image = self.idle_sprite_images_1[int(self.animation_index)]
        elif self.rank == 2:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.idle_sprite_images_2):
                self.animation_index = 0
            self.image = self.idle_sprite_images_2[int(self.animation_index)]
        else:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.idle_sprite_images_3):
                self.animation_index = 0
            self.image = self.idle_sprite_images_3[int(self.animation_index)]
    
    def collision_enemy(self, enemies):
        for enemy in enemies:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.circle_range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                self.target.health -= self.hurt
                print(self.target.health)
                break
    
    def update_rank(self) -> None:
        if self.rank < 3:
            self.rank += 1
            self.create_rank()
            self.create_range()
    
    def update(self, enemies) -> None:
        self.play_animation()
        self.collision_enemy(enemies)
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(pygame.transform.rotate(self.image, self.angle - 90), self.rect)
        if self.selected:
            screen.blit(self.range_image, self.range_rect)