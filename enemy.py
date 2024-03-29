import os
import pygame
import setting
import math
from pygame.math import Vector2
from enemy_data import *

def load_enemy_sprite_sheets(enemy_type) -> list[pygame.Surface]:
    sprite_sheets = list()
    
    for state in setting.ENEMY_STATE:
        if enemy_type == "Slime":
            sprite_sheets.append(pygame.image.load(os.path.join("assets", "enemies", "1", f"D_{state}.png")).convert_alpha())
        elif enemy_type == "Goblin":
            sprite_sheets.append(pygame.image.load(os.path.join("assets", "enemies", "2", f"D_{state}.png")).convert_alpha())
        elif enemy_type == "Wolf":
            sprite_sheets.append(pygame.image.load(os.path.join("assets", "enemies", "3", f"D_{state}.png")).convert_alpha())
        else:
            sprite_sheets.append(pygame.image.load(os.path.join("assets", "enemies", "4", f"D_{state}.png")).convert_alpha())
    
    return sprite_sheets

class Slime(pygame.sprite.Sprite):
    def __init__(self, rank_num, trailhead) -> None:
        super().__init__()
        self.trailhead = trailhead
        self.rank_num = rank_num
        self.speed = RANK[self.rank_num - 1].get("speed")
        self.hurt = RANK[self.rank_num - 1].get("hurt")
        self.health = RANK[self.rank_num - 1].get("health")
        self.reward = RANK[self.rank_num - 1].get("reward")
        self.score = RANK[self.rank_num - 1].get("score")
        self.pos = Vector2(self.trailhead[0])
        self.targetmove = None
        self.movement = None
        self.targetmove_waypoint = 1
        self.angle = 0
        self.sprite_sheets = load_enemy_sprite_sheets(self.__class__.__name__)
        self.process_sheets()
        
        self.animation_index = 0
        self.animation_speed = 0.07
        
        self.dead_animation_index = 0
        self.dead_animation_speed = 0.07
        
        self.image = pygame.transform.rotate(self.walk_sprite_sheet_images[0], self.angle)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
    
    def process_sheets(self):
        self.walk_sprite_sheet_images = list()
        for i in range(6):
            self.walk_sprite_sheet_images.append(self.sprite_sheets[0].subsurface(i * setting.ENEMY_SIZE, 0, setting.ENEMY_SIZE, setting.ENEMY_SIZE))
            
    def move(self, level_health):
        if self.targetmove_waypoint < len(self.trailhead):
            self.targetmove = Vector2(self.trailhead[self.targetmove_waypoint])
            self.movement = self.targetmove - self.pos
        else:
            self.health = 0
            level_health(self.hurt)
            self.kill()

        distance = self.movement.length()
        if distance >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if distance != 0:
                self.pos -= self.movement.normalize() * distance
            self.targetmove_waypoint += 1
        self.rect.topleft = (self.pos.x, self.pos.y)
    
    def play_animation(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.walk_sprite_sheet_images):
            self.animation_index = 0
        self.image = self.walk_sprite_sheet_images[int(self.animation_index)]
    
    def is_dead(self, plus):
        if self.health <= 0:
            plus(self.reward, self.score)
            self.kill()
    
    def update(self, level_health, money_plus) -> None:
        self.is_dead(money_plus)
        if self.health > 0:
            self.move(level_health)
        self.play_animation()
    
class Goblin(Slime):
    def __init__(self, rank_num, trailhead) -> None:
        super().__init__(rank_num, trailhead)

class Wolf(Goblin):
    def __init__(self, rank_num, trailhead) -> None:
        super().__init__(rank_num, trailhead)
    
    def play_animation(self):
        distance = self.targetmove - self.pos
        self.angle = math.degrees(math.atan2(-distance[1], distance[0])) + 90
        
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.walk_sprite_sheet_images):
            self.animation_index = 0
        self.image = self.walk_sprite_sheet_images[int(self.animation_index)]
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

class Bee(Wolf):
    def __init__(self, rank_num, trailhead) -> None:
        super().__init__(rank_num, trailhead)
