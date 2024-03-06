import math
import os
import pygame
import setting
from turret_rank import RANK

class Turret(pygame.sprite.Sprite):
    def load_images(self) -> None:
        self.idle_sprite_images_1 = list()
        self.attack_sprite_images_1_down = list()
        self.attack_sprite_images_1_left = list()
        self.attack_sprite_images_1_up = list()
        
        self.idle_sprite_images_2 = list()
        self.attack_sprite_images_2_down = list()
        self.attack_sprite_images_2_left = list()
        self.attack_sprite_images_2_up = list()
        
        self.idle_sprite_images_3 = list()
        self.attack_sprite_images_3_down = list()
        self.attack_sprite_images_3_left = list()
        self.attack_sprite_images_3_up = list()
        
        idle_sprite_sheet_images_1 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Idle.png")).convert_alpha()
        attack_sprite_sheet_images_1_down = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Attack.png")).convert_alpha()
        attack_sprite_sheet_images_1_left = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "S_Attack.png")).convert_alpha()
        attack_sprite_sheet_images_1_up = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "U_Attack.png")).convert_alpha()

        idle_sprite_sheet_images_2 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "2", "D_Idle.png")).convert_alpha()
        attack_sprite_sheet_images_2_down = pygame.image.load(os.path.join("assets", "towers", "3 Units", "2", "D_Attack.png")).convert_alpha()
        attack_sprite_sheet_images_2_left = pygame.image.load(os.path.join("assets", "towers", "3 Units", "2", "S_Attack.png")).convert_alpha()
        attack_sprite_sheet_images_2_up = pygame.image.load(os.path.join("assets", "towers", "3 Units", "2", "U_Attack.png")).convert_alpha()
    
        idle_sprite_sheet_images_3 = pygame.image.load(os.path.join("assets", "towers", "3 Units", "3", "D_Idle.png")).convert_alpha()
        attack_sprite_sheet_images_3_down = pygame.image.load(os.path.join("assets", "towers", "3 Units", "3", "D_Attack.png")).convert_alpha()
        attack_sprite_sheet_images_3_left = pygame.image.load(os.path.join("assets", "towers", "3 Units", "3", "S_Attack.png")).convert_alpha()
        attack_sprite_sheet_images_3_up = pygame.image.load(os.path.join("assets", "towers", "3 Units", "3", "U_Attack.png")).convert_alpha()
        
        
        for idle_image in range(4):
            self.idle_sprite_images_1.append(idle_sprite_sheet_images_1.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.idle_sprite_images_2.append(idle_sprite_sheet_images_2.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.idle_sprite_images_3.append(idle_sprite_sheet_images_3.subsurface(idle_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            
        for attack_image in range(6):
            self.attack_sprite_images_1_down.append(attack_sprite_sheet_images_1_down.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.attack_sprite_images_2_down.append(attack_sprite_sheet_images_2_down.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.attack_sprite_images_3_down.append(attack_sprite_sheet_images_3_down.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))

            self.attack_sprite_images_1_left.append(attack_sprite_sheet_images_1_left.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.attack_sprite_images_2_left.append(attack_sprite_sheet_images_2_left.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.attack_sprite_images_3_left.append(attack_sprite_sheet_images_3_left.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))

            self.attack_sprite_images_1_up.append(attack_sprite_sheet_images_1_up.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.attack_sprite_images_2_up.append(attack_sprite_sheet_images_2_up.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))
            self.attack_sprite_images_3_up.append(attack_sprite_sheet_images_3_up.subsurface(attack_image * setting.TURRET_SIZE, 0, setting.TURRET_SIZE, setting.TURRET_SIZE))

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
        self.attack_animation_index = 0
        self.attack_animation_speed = 0.07
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
        self.range_rect = self.range_image.get_rect(center=self.rect.center)
    
    def play_idle_animation(self) -> None:
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
    
    def play_attack_animation(self, distance: int):
        if distance == 1:
            if self.rank == 1:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_1_left):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_1_left[int(self.attack_animation_index)]
            elif self.rank == 2:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_2_left):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_2_left[int(self.attack_animation_index)]
            else:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_3_left):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_3_left[int(self.attack_animation_index)]
        elif distance == 2:
            if self.rank == 1:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_1_left):
                    self.attack_animation_index = 0
                self.image = pygame.transform.flip(self.attack_sprite_images_1_left[int(self.attack_animation_index)], True, False)
            elif self.rank == 2:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_2_left):
                    self.attack_animation_index = 0
                self.image = pygame.transform.flip(self.attack_sprite_images_2_left[int(self.attack_animation_index)], True, False)
            else:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_3_left):
                    self.attack_animation_index = 0
                self.image = pygame.transform.flip(self.attack_sprite_images_3_left[int(self.attack_animation_index)], True, False)
        elif distance == 3:
            if self.rank == 1:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_1_down):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_1_down[int(self.attack_animation_index)]
            elif self.rank == 2:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_2_down):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_2_down[int(self.attack_animation_index)]
            else:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_3_down):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_3_down[int(self.attack_animation_index)]
        else:
            if self.rank == 1:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_1_up):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_1_up[int(self.attack_animation_index)]
            elif self.rank == 2:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_2_up):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_2_up[int(self.attack_animation_index)]
            else:
                self.attack_animation_index += self.attack_animation_speed
                if self.attack_animation_index >= len(self.attack_sprite_images_3_up):
                    self.attack_animation_index = 0
                self.image = self.attack_sprite_images_3_up[int(self.attack_animation_index)]

    def shoot_enemy(self, enemies):
        for enemy in enemies:
            if enemy.rect.centerx < self.rect.centerx:
                self.play_attack_animation(1)
            elif enemy.rect.centerx > self.rect.centerx:
                self.play_attack_animation(2)
            elif enemy.rect.centery < self.rect.centery:
                self.play_attack_animation(4)
            elif enemy.rect.centery > self.rect.centery:
                self.play_attack_animation(3)
    
    def update_rank(self) -> None:
        if self.rank < 3:
            self.rank += 1
            self.create_rank()
            self.create_range()
    
    def update(self, enemies) -> None:
        if self.rank == 1:
            ene = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle_ratio(1.35))
        elif self.rank == 2:
            ene = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle_ratio(1.55))
        else:
            ene = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle_ratio(1.8))
        if ene:
            print(ene)
            self.shoot_enemy(ene)
        else:
            self.play_idle_animation()
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        if self.selected:
            screen.blit(self.range_image, self.range_rect)