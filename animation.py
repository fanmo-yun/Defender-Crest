import pygame

class Animation:
    def __init__(self, frames, speed) -> None:
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.speed:
            self.last_frame_time = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_frame(self):
        self.update()
        return self.frames[self.current_frame]