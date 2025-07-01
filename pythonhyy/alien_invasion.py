import pygame
import sys  # 导入系统模块，用于实现游戏退出等系统级操作
import time
from time import sleep  # 导入时间模块，用于实现延时功能
from settings import Settings  # 导入游戏设置类，管理游戏参数
from ship import Ship        # 导入玩家飞船类，控制飞船行为
from bullet import Bullet    # 导入子弹类，管理子弹发射与移动
from alien import Alien      # 导入外星人类，管理外星人行为
from game_stats import GameStats  # 导入游戏状态类，跟踪游戏数据
from button import Button    # 导入按钮类，创建交互按钮
from scoreboard import Scoreboard  # 导入计分板类，显示游戏信息
from music import GameAudio  # 导入音频类，管理游戏音效和音乐
from show_text import show_text  # 导入文本显示函数，显示提示信息
from resource_path import resource_path


class AlienInvasion:
    '''管理游戏资源和行为的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()  # 初始化pygame
        pygame.mixer.init()  # 初始化音频系统
        self.settings=Settings()
        self.clock = pygame.time.Clock()  # 创建时钟对象控制游戏帧率

        # 创建游戏窗口
        self.screen=pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height)
        )                                       
        pygame.display.set_caption("Alien Invasion")  # 设置窗口标题
        self._load_background()  # 加载背景图片
        self.stats=GameStats(self)  # 创建游戏统计信息实例
        self.sb=Scoreboard(self)  # 创建记分牌实例
        self.ship=Ship(self)  # 创建飞船实例
        self.bullets=pygame.sprite.Group()  # 创建子弹精灵组
        self.aliens=pygame.sprite.Group()  # 创建外星人精灵组

        self._create_fleet()  # 创建外星人舰队

        self.play_button=Button(self,"Play")  # 创建Play按钮
        self.paused=False  # 游戏暂停标志

        # 初始化和播放音频
        self.audio=GameAudio()
        self.audio.load_audio() 
        self.audio.play_music()

    def _load_background(self):
        """加载背景图片并适应屏幕尺寸"""
        try:
            background_path=resource_path(r'images\back.jpg')
            self.background = pygame.image.load(background_path).convert()
            self.background = pygame.transform.scale(
                self.background,
                (self.settings.screen_width, self.settings.screen_height)
            )
            
        except FileNotFoundError:
            # 如果图片加载失败，使用纯色背景
            self.background = None
            self.bg_color = (0, 0, 50)  # 深蓝色
            print("wrong")

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_events()  # 检查事件
            if self.stats.game_active:  # 如果游戏处于活动状态
                self.ship.update()  # 更新飞船位置
                self._update_bullets()  # 更新子弹
                self._update_aliens()  # 更新外星人

            self._update_screen()  # 更新屏幕
    
    def _check_events(self):
        #响应按键和鼠标事件
        for event in pygame.event.get():    
            if event.type==pygame.QUIT:  # 如果点击关闭按钮
                sys.exit()                  
            elif event.type==pygame.KEYDOWN:  # 按键按下
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:  # 按键松开
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:  # 鼠标点击
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def pause_game(self):
        """游戏暂停功能"""
        self.paused = True
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:  # 按2继续
                        self.paused = False
                    
    def _check_play_button(self,mouse_pos):
        """检查是否点击了Play按钮"""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            # 清空游戏元素
            self.aliens.empty()
            self.bullets.empty()
            
            # 创建新游戏
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)  # 隐藏鼠标光标

    def _check_keydown_events(self,event):
        """响应按键按下"""
        if event.key == pygame.K_RIGHT:  # 右箭头键
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # 左箭头键
            self.ship.moving_left = True
        elif event.key==pygame.K_1:     # 按1结束游戏
            sys.exit()
        elif event.key==pygame.K_2:  # 按2暂停
            self.pause_game()
        elif event.key==pygame.K_SPACE:  # 空格键发射子弹
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """响应按键松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """发射子弹"""
        self.audio.play_shoot()  # 播放射击音效
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """更新屏幕上的图像"""
        self.screen.blit(self.background, (0, 0))  # 绘制背景
        self.ship.blitme()  # 绘制飞船
        
        # 绘制所有子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # 绘制外星人
        self.sb.show_score()  # 显示得分

        # 如果游戏处于非活动状态，绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  # 更新显示

    def _update_bullets(self):
        """更新子弹位置并删除消失的子弹"""
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
 
    def _check_bullet_alien_collisions(self):
        """检查子弹和外星人的碰撞"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.audio.play_crash()  # 播放碰撞音效
            # 计算得分
            for aliens in collisions.values():
                self.stats.score += self .settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            
        if not self.aliens:
            # 如果消灭了所有外星人
            self.bullets.empty()
            show_text(self.screen, self.background, "恭喜你进入下一关卡！")
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
     
    def _create_fleet(self):
        """创建外星人群"""
        for _ in range(10):  
            alien = Alien(self)
            self.aliens.add(alien)

    def _create_alien(self,alien_number,row_number):
        """创建一个外星人并放入当前行"""
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width+2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """检查外星人是否到达边缘"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        self.audio.play_hit()  # 播放撞击音效
        if self.stats.ships_left>0:
            # 将ships_left减1
            self.stats.ships_left-=1
            self.sb.prep_ships()

            # 清空外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的外星人群，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()

            show_text(self.screen, self.background, "再接再厉！！")
                
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break

if __name__=='__main__':
    # 创建游戏实例并运行游戏
    ai=AlienInvasion()
    ai.run_game()