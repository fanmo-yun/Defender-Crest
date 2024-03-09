import os
import pygame
import setting
from animation import Animation
from button import GameButton

class Camp:
    def load_camp_image(self):
        temp_file = list()
        for i in range(1, 8):
            temp_file.append(pygame.image.load(os.path.join("assets", "towers", "2 Idle", f"{i}.png")).convert_alpha())
        temp_file.append(pygame.image.load(os.path.join("assets", "tileset", "3 Animated Objects", "2 Campfire", "2.png")).convert_alpha())
        for i in range(1, 3):
            temp_file.append(pygame.image.load(os.path.join("assets", "tileset", "2 Objects", "8 Camp", f"{i}.png")).convert_alpha())
        
        self.tower1 = temp_file[0]
        self.tower2 = Animation([temp_file[1].subsurface(setting.TOWER_WIDTH_SIZE * i, 0, setting.TOWER_WIDTH_SIZE, setting.TOWER_HEIGHT_SIZE) for i in range(4)], 300)
        self.tower3 = Animation([temp_file[2].subsurface(setting.TOWER_WIDTH_SIZE * i, 0, setting.TOWER_WIDTH_SIZE, setting.TOWER_HEIGHT_SIZE) for i in range(4)], 300)
        self.tower4 = Animation([temp_file[3].subsurface(setting.TOWER_WIDTH_SIZE * i, 0, setting.TOWER_WIDTH_SIZE, setting.TOWER_HEIGHT_SIZE) for i in range(6)], 300)
        self.tower5 = Animation([temp_file[4].subsurface(setting.TOWER_WIDTH_SIZE * i, 0, setting.TOWER_WIDTH_SIZE, setting.TOWER_HEIGHT_SIZE) for i in range(6)], 300)
        self.tower6 = Animation([temp_file[5].subsurface(setting.TOWER_WIDTH_SIZE * i, 0, setting.TOWER_WIDTH_SIZE, setting.TOWER_HEIGHT_SIZE) for i in range(6)], 300)
        self.tower7 = Animation([temp_file[6].subsurface(setting.TOWER_WIDTH_SIZE * i, 0, setting.TOWER_WIDTH_SIZE, setting.TOWER_HEIGHT_SIZE) for i in range(6)], 300)
        
        self.campfire = Animation([temp_file[7].subsurface(setting.TILE_SIZE * i, 0, setting.TILE_SIZE, setting.TILE_SIZE) for i in range(4)], 200)
        self.camp1 = temp_file[8]
        self.camp2 = temp_file[9]
        
    def __init__(self) -> None:
        self.update_times = [10, 15, 20]
        self.spend_money = [30, 80, 120]
        self.update_state = 0
        self.camp_image = pygame.image.load(os.path.join("maps", "upgradecamp", "upgradecamp.png"))
        self.update_button = GameButton((128, 128, 0), setting.WHITE, "UpdateCamp", (130, 35), (setting.SCREEN_WIDTH + 10, 30))
        self.back_button = GameButton((220, 20, 60), setting.WHITE, "Back", (130, 35), (setting.SCREEN_WIDTH + 10, setting.SCREEN_HEIGHT - 60))
        
        self.load_camp_image()
    
    def draw_image(self):
        pass

    def update_states(self):
        self.update_state += 1
    
    def update_camp(self, update_spend):
        if self.update_state < 3:
            update_spend(self.spend_money[self.update_state], self.update_times[self.update_state], self.update_states)
    
    def state0(self, screen: pygame.Surface):
        screen.blit(self.camp1, (530, 320))
        screen.blit(self.camp2, (480, 250))
    
    def state1(self, screen: pygame.Surface):
        screen.blit(self.tower1, (460, 300))
        screen.blit(self.tower1, (400, 250))
        screen.blit(self.tower2.get_current_frame(), (520, 250))
        screen.blit(self.tower3.get_current_frame(), (460, 180))
    
    def state2(self, screen: pygame.Surface):
        screen.blit(self.tower3.get_current_frame(), (460, 300))
        screen.blit(self.tower4.get_current_frame(), (400, 250))
        screen.blit(self.tower4.get_current_frame(), (520, 250))
        screen.blit(self.tower5.get_current_frame(), (460, 180))
        
        screen.blit(self.tower1, (600, 250))
        screen.blit(self.tower1, (460, 90))
        screen.blit(self.tower2.get_current_frame(), (570, 160))
        screen.blit(self.tower2.get_current_frame(), (350, 160))
        screen.blit(self.tower4.get_current_frame(), (460, 390))
        screen.blit(self.tower4.get_current_frame(), (350, 340))
        screen.blit(self.tower4.get_current_frame(), (570, 340))
        
    def state3(self, screen: pygame.Surface):
        screen.blit(self.tower5.get_current_frame(), (460, 300))
        screen.blit(self.tower6.get_current_frame(), (400, 250))
        screen.blit(self.tower4.get_current_frame(), (520, 250))
        screen.blit(self.tower5.get_current_frame(), (460, 180))
        
        screen.blit(self.tower7.get_current_frame(), (620, 250))
        screen.blit(self.tower7.get_current_frame(), (460, 90))
        screen.blit(self.tower7.get_current_frame(), (570, 160))
        screen.blit(self.tower6.get_current_frame(), (350, 160))
        screen.blit(self.tower7.get_current_frame(), (460, 390))
        screen.blit(self.tower5.get_current_frame(), (350, 340))
        screen.blit(self.tower4.get_current_frame(), (570, 340))
        
        screen.blit(self.tower4.get_current_frame(), (300, 250))
        screen.blit(self.tower6.get_current_frame(), (640, 100))
        screen.blit(self.tower6.get_current_frame(), (320, 420))
        screen.blit(self.tower6.get_current_frame(), (550, 430))
        screen.blit(self.tower7.get_current_frame(), (280, 110))

    def tower_state(self, screen: pygame.Surface):
        if self.update_state == 0:
            self.state0(screen)
        elif self.update_state == 1:
            self.state1(screen)
        elif self.update_state == 2:
            self.state2(screen)
        else:
            self.state3(screen)

    def draw(self, screen: pygame.Surface, cancel_mode, update_spend):
        if self.update_button.draw(screen):
            self.update_camp(update_spend)
        if self.back_button.draw(screen):
            cancel_mode()
        
        screen.blit(self.camp_image, (0, 0))
        screen.blit(self.campfire.get_current_frame(), (setting.SCREEN_WIDTH // 2, setting.SCREEN_HEIGHT // 2))
        self.tower_state(screen)
