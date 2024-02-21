import pygame
import setting

pygame.init()
screen = pygame.display.set_mode((setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT))
pygame.display.set_caption("Defender Crest")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(setting.WHITE)
    pygame.display.flip()

pygame.quit()
