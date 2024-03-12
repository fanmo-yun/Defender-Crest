import os
import pygame
import setting
import json
import random
from camp import Camp
from turret import Turret
from gameover import GameOver
from button import GameButton
from enemy_data import GENERATE
from enemy import Slime, Goblin, Wolf, Bee

class Level_1:
    def __init__(self) -> None:
        self.load_data()
        self.score = 0
        self.clicked = False
        self.create = False
        self.selected = False
        self.choose_turret = None
        self.is_pass_game = False
        self.game_over = False
        self.camp = False
        self.last_generate_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(os.path.join("font", "JetBrainsMono-Bold.ttf"), 20)
        self.life_image = pygame.image.load(os.path.join("assets", "life" ,"life.png")).convert_alpha()
        self.buy_turret_button = GameButton((128, 128, 0), setting.WHITE, "Buy", (130, 35), (setting.SCREEN_WIDTH + 10, 30))
        self.cancel_turret_button = GameButton((220, 20, 60), setting.WHITE, "Cancel", (130, 35), (setting.SCREEN_WIDTH + 10, 70))
        self.upgrade_turret_button = GameButton((255, 140, 0), setting.WHITE, "Upgrade", (130, 35), (setting.SCREEN_WIDTH + 10, 110))
        self.sell_turret_button = GameButton((211, 211, 211), setting.WHITE, "Sell", (130, 35), (setting.SCREEN_WIDTH + 10, 150))
        self.camp_button = GameButton((255, 204, 0), setting.WHITE, "Go to Camp", (130, 35), (setting.SCREEN_WIDTH + 10, setting.SCREEN_HEIGHT - 60))
        self.turrets_group = pygame.sprite.Group()
        self.enemys_group = pygame.sprite.Group()
        self.camp_mode = Camp()
        
        self.load_level_image()
        self.load_level_data()
        self.load_coin_image()
        self.load_turret_num_image()
        self.load_turret()
        self.load_enemies()
    
    def load_level_image(self):
        self.level_image = pygame.image.load(os.path.join("maps", "level1", "level1.png")).convert_alpha()
    
    def load_data(self):
        with open(os.path.join("maps", "level1", "level1.json"), "r", encoding="UTF-8") as fp:
            data = fp.read()
        
        self.json_data = json.loads(data)
        self.tile_data = self.json_data["layers"][0]["data"]
        self.trailhead = [(-35, 433), (90, 433), (90, 90), (410, 90), (410, 500), (725, 500), (725, 250), (930, 250)]
    
    def load_level_data(self):
        self.money = 80
        self.turret_num = 15
        self.level_health = 100
    
    def load_turret_num_image(self):
        self.turret_num_sheet_image = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "S_Idle.png")).convert_alpha()
        self.num_subsurface_rect = pygame.Rect(0, 0, 48, 48)
        self.num_sprite_subsurface = self.turret_num_sheet_image.subsurface(self.num_subsurface_rect)
    
    def load_coin_image(self):
        self.coin_image = pygame.image.load(os.path.join("assets", "coin", "GoldCoinSpinning.png")).convert_alpha()
        self.coin_subsurface_rect = pygame.Rect(0, 0, 8, 8)
        self.coin_sprite_subsurface = self.coin_image.subsurface(self.coin_subsurface_rect)
    
    def load_turret(self):
        self.turret_sprite_sheet_image = pygame.image.load(os.path.join("assets", "towers", "3 Units", "1", "D_Idle.png")).convert_alpha()
        self.subsurface_rect = pygame.Rect(0, 0, 48, 48)
        self.sprite_subsurface = self.turret_sprite_sheet_image.subsurface(self.subsurface_rect)
        self.sprite_subsurface_rect = self.sprite_subsurface.get_rect()
    
    def load_enemies(self):
        self.generate_level = 0
        self.enemy_num = list()
        for num in GENERATE[self.generate_level]:
            self.enemy_num.append(GENERATE[self.generate_level][num])

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
    
    def check_tile(self, mouse_set_tile_num: int) -> bool:
        if self.tile_data[mouse_set_tile_num] == 38:
            return True
        return False
    
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
                    if self.check_tile(mouse_set_tile_num):
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
    
    def generate_enemies_num(self):
        self.enemy_rank_num = random.randint(1, 1)
    
    def generate_enemies(self):
        self.generate_enemies_num()
        self.choose_enemy = random.randint(0, 3)
        if pygame.time.get_ticks() - self.last_generate_time >= random.randint(1500, 8000):
            if self.choose_enemy == 0:
                if self.enemy_num[self.choose_enemy] >= 0:
                    self.enemys_group.add(Slime(self.enemy_rank_num, self.trailhead))
                    self.enemy_num[self.choose_enemy] -= 1
            elif self.choose_enemy == 1:
                if self.enemy_num[self.choose_enemy] >= 0:
                    self.enemys_group.add(Goblin(self.enemy_rank_num, self.trailhead))
                    self.enemy_num[self.choose_enemy] -= 1
            elif self.choose_enemy == 2:
                if self.enemy_num[self.choose_enemy] >= 0:
                    self.enemys_group.add(Wolf(self.enemy_rank_num, self.trailhead))
                    self.enemy_num[self.choose_enemy] -= 1
            elif self.choose_enemy == 3:
                if self.enemy_num[self.choose_enemy] >= 0:
                    self.enemys_group.add(Bee(self.enemy_rank_num, self.trailhead))
                    self.enemy_num[self.choose_enemy] -= 1
            
            self.last_generate_time = pygame.time.get_ticks()

    def pass_game(self):
        if self.enemy_num[0] <= 0 and self.enemy_num[1] <= 0 and self.enemy_num[2] <= 0 and self.enemy_num[3] <= 0 and len(self.enemys_group) <= 0:
            self.is_pass_game = True
    
    def is_game_over(self):
        if self.level_health <= 0:
            self.game_over = True
    
    def level_health_minus(self, enemy_hurt: int):
        self.level_health -= enemy_hurt
    
    def level_money_plus(self, reward: int, sco: int):
        self.money += reward
        self.score += sco
    
    def update_turret_money(self, spend: int):
        self.money -= spend
    
    def level_money_minus(self, spend: int, add_num: int, update_camp):
        if self.money - spend > 0:
            self.money -= spend
            self.turret_num += add_num
            update_camp()
    
    def not_camp(self):
        self.camp = False
    
    def draw_num_images(self, screen: pygame.Surface):
        screen.blit(pygame.transform.scale(self.life_image, (25, 25)), (3, 7))
        screen.blit(self.num_sprite_subsurface, (68, 2))
        screen.blit(pygame.transform.scale(self.coin_sprite_subsurface, (25, 25)), (145, 8))
        
        screen.blit(self.font.render(str(int(self.level_health)), True, setting.WHITE), (35, 7))
        screen.blit(self.font.render(str(self.turret_num), True, setting.WHITE), (108, 7))
        screen.blit(self.font.render(str(self.money), True, setting.WHITE), (175, 7))
    
    def draw_screen(self, screen: pygame.Surface):
        if self.buy_turret_button.draw(screen):
            if self.money > 0 and self.turret_num > 0:
                if self.choose_turret != None:
                    self.reject_all()
                self.money -= 5
                self.turret_num -= 1
                self.create = True
                self.selected = False

        if self.selected:
            if self.cancel_turret_button.draw(screen):
                self.reject_all()
                self.selected = False
            if self.upgrade_turret_button.draw(screen):
                if self.money - self.choose_turret.cost > 0:
                    self.choose_turret.update_rank(self.update_turret_money)
            if self.sell_turret_button.draw(screen):
                self.choose_turret.kill()
                self.money += self.choose_turret.sell
                self.turret_num += 1
                self.selected = False
        if self.camp_button.draw(screen):
            self.camp = True

        screen.blit(self.level_image, (0, 0))
        self.enemys_group.update(self.level_health_minus, self.level_money_plus)
        self.enemys_group.draw(screen)
        self.turrets_group.update(self.enemys_group)
        for turret in self.turrets_group:
            turret.draw(screen)

        self.draw_num_images(screen)
        self.create_or_select_turret(screen)
        self.generate_enemies()
    
    def normal_mode(self, screen: pygame.Surface):
        self.pass_game()
        if self.game_over == False:
            self.is_game_over()
            if self.is_pass_game == False:
                self.draw_screen(screen)
            else:
                self.enemys_group.empty()
                self.turrets_group.empty()
        else:
            self.gameover_level = GameOver()
            self.gameover_level.draw(screen)
    
    def draw(self, screen: pygame.Surface):
        if self.camp == False:
            self.normal_mode(screen)
        else:
            self.camp_mode.draw(screen, self.not_camp, self.level_money_minus)
            self.draw_num_images(screen)

class Level_2(Level_1):
    def __init__(self) -> None:
        super().__init__()
    
    def load_level_image(self):
        self.level_image = pygame.image.load(os.path.join("maps", "level2", "level2.png")).convert_alpha()
    
    def load_data(self):
        with open(os.path.join("maps", "level2", "level2.json"), "r", encoding="UTF-8") as fp:
            data = fp.read()
        
        self.json_data = json.loads(data)
        self.tile_data = self.json_data["layers"][0]["data"]
        self.trailhead = [(-80, 80), (790, 80), (790, 270), (90, 270), (90, 460), (855, 460), (855, 610)]
    
    def check_tile(self, mouse_set_tile_num: int) -> bool:
        if self.tile_data[mouse_set_tile_num] == 84:
            return True
        return False
    
    def load_level_data(self):
        self.money = 120
        self.turret_num = 15
        self.level_health = 120
    
    def generate_enemies_num(self):
        self.enemy_rank_num = random.randint(1, 2)
    
    def load_enemies(self):
        self.generate_level = 1
        self.enemy_num = list()
        for num in GENERATE[self.generate_level]:
            self.enemy_num.append(GENERATE[self.generate_level][num])

class Level_3(Level_1):
    def __init__(self) -> None:
        super().__init__()

    def load_level_image(self):
        self.level_image = pygame.image.load(os.path.join("maps", "level3", "level3.png")).convert_alpha()
    
    def load_data(self):
        with open(os.path.join("maps", "level3", "level3.json"), "r", encoding="UTF-8") as fp:
            data = fp.read()
        
        self.json_data = json.loads(data)
        self.tile_data = self.json_data["layers"][0]["data"]
        self.trailhead = [(-80, 180), (150, 180), (150, 50), (375, 50), (375, 335), (120, 335), (120, 500), (565, 500), (565, 80), (825, 80), (825, 460), (930, 460)]
    
    def check_tile(self, mouse_set_tile_num: int) -> bool:
        if self.tile_data[mouse_set_tile_num] == 87:
            return True
        return False
    
    def load_level_data(self):
        self.money = 180
        self.turret_num = 15
        self.level_health = 180
    
    def generate_enemies_num(self):
        self.enemy_rank_num = random.randint(1, 3)
    
    def load_enemies(self):
        self.generate_level = 2
        self.enemy_num = list()
        for num in GENERATE[self.generate_level]:
            self.enemy_num.append(GENERATE[self.generate_level][num])

class Level_end:
    def __init__(self) -> None:
        self.background_image = pygame.image.load(os.path.join("maps", "end", "end.png")).convert_alpha()
        self.font = pygame.font.Font(os.path.join("font", "JetBrainsMono-Bold.ttf"), 25)
        self.font2 = pygame.font.Font(os.path.join("font", "JetBrainsMono-Bold.ttf"), 22)
        self.thanksplay = self.font.render("Thanks for playing, you can close this window", True, setting.WHITE)
    
    def draw_fonts(self, text: str) -> pygame.Surface:
        return self.font2.render(text, True, setting.WHITE)
    
    def draw(self, screen: pygame.Surface, score):
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.thanksplay, (210, 220))
        screen.blit(self.draw_fonts("LEVEL 1: " + str(score[0])), (480, 270))
        screen.blit(self.draw_fonts("LEVEL 2: " + str(score[1])), (480, 300))
        screen.blit(self.draw_fonts("LEVEL 3: " + str(score[2])), (480, 330))
