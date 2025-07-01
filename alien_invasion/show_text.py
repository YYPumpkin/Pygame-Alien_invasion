import pygame
import sys

def show_text(screen, background, text_content, font_name="SimSun", font_size=80, 
              text_color=(51, 102, 204), display_time=3000, fps=15, 
              overlay_alpha=0):
    """
    在游戏屏幕上显示指定文本一段时间，期间保持游戏响应
    
    参数:
        screen: Pygame屏幕对象
        background: 背景Surface，用于重绘
        text_content: 要显示的文本内容
        font_name: 字体名称
        font_size: 字体大小
        text_color: 文本颜色(RGB元组)
        display_time: 显示时间(毫秒)
        fps: 显示期间的帧率
        overlay_alpha: 遮罩透明度(0-255)
    """
    # 设置字体
    font = pygame.font.SysFont(font_name, font_size)
    # 渲染文本
    text = font.render(text_content, True, text_color)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # 创建半透明遮罩
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, overlay_alpha))  # 半透明黑色
    
    # 记录开始时间
    start_time = pygame.time.get_ticks()
    
    # 创建时钟对象控制帧率
    clock = pygame.time.Clock()
    
    # 显示文字指定时间（非阻塞方式）
    while pygame.time.get_ticks() - start_time < display_time:
        # 处理事件，保持游戏响应
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # 绘制背景、遮罩和文字
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(text, text_rect)
        
        # 更新显示
        pygame.display.flip()
        clock.tick(fps)  # 控制帧率减少CPU占用    