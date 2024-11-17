import pygame, time
from math import *

class AnimationWipe:
    is_completed = False
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.start_pos=(x, y)
        self.rect = pygame.Rect(600, 400, 10, 10)
        self.img = img
        
    def move(self, index, A = 50, max_index=pi*4, omega=10):
        index /= 25
        self.x = self.start_pos[0] + index*omega
        self.y = self.start_pos[1] + A*sin(index)
        if index >= max_index:
            self.is_completed = True

    def draw(self, dst_surf:pygame.Surface):
        dst_surf.blit(self.img, (self.x, self.y))
