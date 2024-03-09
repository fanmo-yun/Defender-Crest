import pygame, os
import setting

pygame.init()
screen = pygame.display.set_mode((setting.SCREEN_WIDTH + setting.BANNER_SIZE, setting.SCREEN_HEIGHT))
pygame.display.set_caption(setting.GAMETITLE)
clock = pygame.time.Clock()

level_image = pygame.image.load(os.path.join("maps", "level2", "level2.png")).convert_alpha()
slime = pygame.image.load("assets\\enemies\\1\\D_Walk.png").convert_alpha()
slime_suf = slime.subsurface(0,0,48,48).convert_alpha()

running = True
while running:
    clock.tick(setting.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(setting.KLEINBLUE)
    screen.blit(level_image, (0, 0))
    [(-80, 80), (790, 80), (790, 270), (90, 270), (410, 500), (90, 460), (855, 460), (855, 610)]
    # screen.blit(slime_suf, (-80, 80))
    # screen.blit(slime_suf, (790, 80))
    # screen.blit(slime_suf, (790, 270))
    # screen.blit(slime_suf, (90, 460))
    screen.blit(slime_suf, (855, 610))
    pygame.display.flip()

pygame.quit()