import pygame.font
from pygame.sprite import Group
from ship import Ship
from resource_path import resource_path

class Scoreboard:
    """游戏计分板类：负责显示分数、等级、剩余飞船等游戏状态信息"""
    
    def __init__(self, ai_game):
        """初始化计分板相关属性"""
        self.ai_game = ai_game                  # 引用游戏主实例
        self.screen = ai_game.screen            # 游戏主屏幕对象
        self.screen_rect = ai_game.screen.get_rect()  # 屏幕矩形边界
        self.settings = ai_game.settings        # 游戏配置参数
        self.stats = ai_game.stats              # 游戏状态统计数据
        
        # 文本样式设置
        self.text_color = (30, 30, 30)          # 文本颜色（深灰色）
        self.font = pygame.font.SysFont(None, 48)  # 使用默认系统字体，大小48
        
        # 初始化各状态显示内容
        self.prep_score()         # 准备当前分数显示
        self.prep_high_score()    # 准备历史最高分显示
        self.prep_level()         # 准备等级显示
        self.prep_ships()         # 准备剩余飞船显示

    def prep_ships(self):
        """创建剩余飞船图标组，显示玩家剩余生命"""
        self.ships = Group()  # 创建飞船精灵组
        # 遍历剩余飞船数量，创建对应数量的飞船图标
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)  # 创建飞船实例
            
            # 加载并设置新的飞船图标（示例：爱心图标）
            icon_path=resource_path(r'images/love.png')
            new_icon = pygame.image.load(icon_path).convert_alpha()
            ship.image = pygame.transform.scale(new_icon, (50, 50))  # 缩放图标尺寸
            
            # 设置图标位置：水平排列在屏幕左上角
            ship.rect.x = 10 + ship_number * ship.rect.width  # 计算水平间距
            ship.rect.y = 10                                 # 顶部边距10像素
            self.ships.add(ship)  # 将图标添加到精灵组

    def prep_level(self):
        """准备等级显示文本"""
        level_str = str(self.stats.level)  # 将等级转换为字符串
        # 渲染等级文本（参数：文本内容、抗锯齿、颜色）
        self.level_image = self.font.render(level_str, True, self.text_color)
        # 设置等级文本位置：在当前分数下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right       # 与分数右对齐
        self.level_rect.top = self.score_rect.bottom + 10  # 分数下方10像素

    def prep_high_score(self):
        """准备历史最高分显示文本"""
        # 对历史最高分进行格式化：四舍五入到最近的10的倍数
        high_score = round(self.stats.high_score, -1)
        # 添加千位分隔符（如10000显示为10,000）
        high_score_str = '{:,}'.format(high_score)
        # 渲染最高分文本
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        # 设置最高分文本位置：屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx  # 水平居中
        self.high_score_rect.top = self.score_rect.top           # 与分数顶部对齐

    def prep_score(self):
        """准备当前分数显示文本"""
        # 对当前分数进行格式化：四舍五入到最近的10的倍数
        rounded_score = round(self.stats.score, -1)
        # 添加千位分隔符
        score_str = '{:,}'.format(rounded_score)
        # 渲染分数文本
        self.score_image = self.font.render(score_str, True, self.text_color)
        # 设置分数文本位置：屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  # 右边界内20像素
        self.score_rect.top = 20                             # 上边界20像素

    def show_score(self):
        """在屏幕上绘制所有计分板元素"""
        self.screen.blit(self.score_image, self.score_rect)      # 绘制当前分数
        self.screen.blit(self.high_score_image, self.high_score_rect)  # 绘制历史最高分
        self.screen.blit(self.level_image, self.level_rect)      # 绘制等级
        self.ships.draw(self.screen)                              # 绘制剩余飞船图标

    def check_high_score(self):
        """检查当前分数是否超过历史最高分，若超过则更新"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score  # 更新历史最高分
            self.prep_high_score()                    # 重新渲染最高分文本