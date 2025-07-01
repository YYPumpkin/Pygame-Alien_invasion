import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船发射子弹的类，继承自Pygame的Sprite类以支持精灵组管理"""
    
    def __init__(self, ai_game):
        """初始化子弹对象，设置其初始位置"""
        super().__init__()  # 调用父类Sprite的初始化方法
        self.screen = ai_game.screen          # 引用游戏主屏幕
        self.settings = ai_game.settings      # 引用游戏设置
        self.color = self.settings.bullet_color  # 获取子弹颜色
        
        # 创建子弹的矩形区域（初始位置在(0,0)）
        self.radius = self.settings.bullet_radius  # 子弹半径（用于圆形绘制）
        bullet_width = self.settings.bullet_width  # 子弹宽度
        bullet_height = self.settings.bullet_height  # 子弹高度
        self.rect = pygame.Rect(0, 0, bullet_width, bullet_height)  # 矩形碰撞盒
        
        # 设置子弹位置：位于飞船顶部中央
        self.rect.midtop = ai_game.ship.rect.midtop  # 使用飞船顶部中央坐标
        
        # 将矩形位置转换为浮点数，用于精确移动计算
        self.y = float(self.rect.y)

    def update(self):
        """更新子弹位置：根据速度向上移动"""
        # 向上移动子弹（y轴向上为负方向）
        self.y -= self.settings.bullet_speed  # 减去速度值实现向上移动
        # 更新矩形位置（整数坐标用于碰撞检测）
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹（使用圆形绘制，更美观）"""
        # 使用pygame.draw.circle绘制圆形子弹
        # 参数：屏幕、颜色、圆心坐标、半径
        pygame.draw.circle(
            self.screen, 
            self.color, 
            (self.rect.centerx, self.rect.centery), 
            self.radius
        )