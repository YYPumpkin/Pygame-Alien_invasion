import pygame
from pygame.sprite import Sprite
from resource_path import resource_path

class Ship(Sprite):
    """玩家飞船类：控制飞船的移动、绘制和位置管理"""
    
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()  # 调用Sprite基类的初始化方法
        self.screen = ai_game.screen          # 游戏主屏幕
        self.settings = ai_game.settings      # 游戏设置参数
        self.screen_rect = ai_game.screen.get_rect()  # 屏幕矩形边界
        
        # 加载飞船图像并获取其矩形区域
        image_path=resource_path(r'images\tank.png')
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()     # 飞船图像的矩形边界
        
        # 设置飞船初始位置：屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom  # 底部居中对齐
        
        # 使用浮点数精确存储飞船水平位置
        self.x = float(self.rect.x)           # 将整数坐标转换为浮点数
        
        # 移动状态标志
        self.moving_right = False  # 向右移动标志
        self.moving_left = False   # 向左移动标志

    def update(self):
        """根据移动标志更新飞船位置（实现平滑移动）"""
        # 向右移动（确保不超出屏幕右边界）
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed  # 根据设置中的速度更新位置
            
        # 向左移动（确保不超出屏幕左边界）
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed  # 根据设置中的速度更新位置
            
        # 将浮点位置转换为整数矩形位置
        self.rect.x = self.x  # Pygame使用整数坐标渲染图形

    def blitme(self):
        """在屏幕上绘制飞船"""
        self.screen.blit(self.image, self.rect)  # 将图像绘制到rect指定的位置

    def center_ship(self):
        """将飞船重置到屏幕底部中央（用于重新开始游戏或生命值减少时）"""
        self.rect.midbottom = self.screen_rect.midbottom  # 重置矩形位置
        self.x = float(self.rect.x)  # 更新浮点位置，确保与矩形位置一致