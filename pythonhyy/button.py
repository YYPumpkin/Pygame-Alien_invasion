import pygame.font

class Button:
    """游戏按钮类，用于创建可交互的开始/暂停等按钮"""
    
    def __init__(self, ai_game, msg):
        """初始化按钮属性并设置外观"""
        self.screen = ai_game.screen          # 引用游戏主屏幕
        self.screen_rect = self.screen.get_rect()  # 获取屏幕矩形边界
        
        # 按钮尺寸和颜色设置
        self.width, self.height = 200, 50      # 按钮宽高（像素）
        self.button_color = (51, 102, 204)     # 按钮背景色（蓝色）
        self.text_color = (255, 255, 255)      # 文本颜色（白色）
        self.font = pygame.font.SysFont(None, 48)  # 使用默认系统字体，大小48
        
        # 创建按钮的矩形区域并居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # 按钮矩形
        self.rect.center = self.screen_rect.center  # 按钮在屏幕中央
        
        # 准备按钮显示的文本内容
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将文本渲染为图像，便于在按钮上绘制"""
        # 渲染文本：参数依次为（文本内容、抗锯齿、文本颜色、背景颜色）
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()  # 获取文本图像的矩形区域
        # 设置文本图像在按钮上的位置：居中显示
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """在屏幕上绘制按钮：先画背景矩形，再画文本图像"""
        self.screen.fill(self.button_color, self.rect)  # 绘制按钮背景
        self.screen.blit(self.msg_image, self.msg_image_rect)  # 绘制文本图像