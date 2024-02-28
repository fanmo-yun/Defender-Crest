import pygame
import setting
from homepage import HomePage

pygame.init()
screen = pygame.display.set_mode((setting.SCREEN_WIDTH + setting.BANNER_SIZE, setting.SCREEN_HEIGHT))
pygame.display.set_caption(setting.GAMETITLE)
clock = pygame.time.Clock()

homepage = HomePage()

running = True
while running:
    clock.tick(setting.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(setting.KLEINBLUE)
    homepage.draw(screen)
    pygame.display.flip()

pygame.quit()
