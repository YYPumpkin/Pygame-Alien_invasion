import pygame
import random
from pygame.sprite import Sprite
from resource_path import resource_path

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        image_path=resource_path(r'images/boat.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        
        # 初始随机位置（避免太靠近边界）
        self.rect.x = random.randint(50, self.settings.screen_width - 50)
        self.rect.y = random.randint(-100, -40)  # 从屏幕上方随机位置出现
        
        # 随机移动参数
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_x = random.uniform(0.5, 1.5) * self.settings.alien_speed
        self.speed_y = random.uniform(0.2, 0.5) * self.settings.alien_speed
        self.direction_x = random.choice([-1, 1])  # 初始随机左右方向
        self.direction_y = 1  # 默认向下移动

    def update(self):
        """随机移动逻辑"""
        # 水平移动（随机左右晃动）
        self.x += self.speed_x * self.direction_x
        self.rect.x = int(self.x)
        
        # 垂直移动（缓慢向下）
        self.y += self.speed_y * self.direction_y
        self.rect.y = int(self.y)
        

    def check_edges(self):
        """检测屏幕边界"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            self.direction_x *= -1  # 碰到左右边界就反弹
        if self.rect.bottom >= screen_rect.bottom:
            return True  # 通知主程序敌人到达底部
        return False