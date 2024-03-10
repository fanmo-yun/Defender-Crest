import os
import sys
import pygame
import setting
from button import Button

class GameOver:
    def __init__(self) -> None:
        self.game_over_image = pygame.image.load(os.path.join("maps", "gameover", "gameover.png")).convert_alpha()
        self.font = pygame.font.Font(os.path.join("font", "JetBrainsMono-Bold.ttf"), 20)
        self.text = self.font.render("You can close this window and restart the game!", True, setting.WHITE)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.game_over_image, (0, 0))
        screen.blit(self.text, (280, 300))