class Settings:
    def __init__(self):
        '''初始化游戏的设置'''
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(255,255,255)

        self.ship_limit=3

        self.bullet_radius=10
        self.bullet_width=10
        self.bullet_height=15
        self.bullet_color=(0,0,180)
        self.bullets_allowed=3

        self.fleet_drop_speed=5

        self.speedup_scale=1.2
        self.score_scale=1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.alien_speed=0.1
        self.fleet_direction=1
        self.alien_points=50

    def increase_speed(self):
        self.ship_speed*=1
        self.bullet_speed*=1
        self.alien_speed*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)
        print(self.alien_points)