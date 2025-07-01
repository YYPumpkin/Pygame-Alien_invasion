import pygame
import os
from resource_path import resource_path

class GameAudio:
    def __init__(self):
        """初始化音频系统"""
        pygame.mixer.init()
        
        # 音频资源
        self.bg_music = None      # 背景音乐
        self.shoot_sound = None   # 子弹发射音效
        self.hit_sound = None     # 子弹击中音效
        self.crash_sound = None  # 子弹击中外星人音效
        
        # 音量设置（可按需调整）
        self.music_volume =0.5  # 背景音乐音量(0.0-1.0)
        self.sfx_volume = 0.2    # 音效音量(0.0-1.0)
        
        # 开关状态
        self.music_on = True
        self.sfx_on = True

    def load_audio(self, audio_dir="audio"):
        try:
            # 1. 加载背景音乐 - 替换为你的文件名
            music_subdir="music"
            bg_path = resource_path(os.path.join(audio_dir,music_subdir,"background.mp3"))
            if os.path.exists(bg_path):
                pygame.mixer.music.load(bg_path)
                pygame.mixer.music.set_volume(self.music_volume)
            else:
                print(f"警告：背景音乐文件未找到于 '{bg_path}'")
            
            # 2. 加载子弹发射音效 - 替换为你的文件名
            shoot_path = resource_path(os.path.join(audio_dir,music_subdir,"shipbullet.wav"))
            if os.path.exists(shoot_path):
                self.shoot_sound = pygame.mixer.Sound(shoot_path)
                self.shoot_sound.set_volume(self.sfx_volume)
            else:
                print(f"警告：射击音效文件未找到于 '{shoot_path}'")

            
            # 3. 加载击中音效 - 替换为你的文件名
            hit_path = resource_path(os.path.join(audio_dir,music_subdir,"boom.mp3"))
            if os.path.exists(hit_path):
                self.hit_sound = pygame.mixer.Sound(hit_path)
                self.hit_sound.set_volume(self.sfx_volume)
            else:
                print(f"警告：撞击音效(hit)文件未找到于 '{hit_path}'")



            crash_path = resource_path(os.path.join(audio_dir,music_subdir,"bulletsound.wav"))
            if os.path.exists(crash_path):
                self.crash_sound = pygame.mixer.Sound(crash_path)
                self.crash_sound.set_volume(self.sfx_volume)
            else:
                print(f"警告：碰撞音效(crash)文件未找到于 '{crash_path}'")


                
        except Exception as e:
            print(f"音频加载错误: {e}")

    def play_music(self, loops=-1):
        """播放背景音乐(-1=循环)"""
        if self.music_on and pygame.mixer.music.get_busy() == 0:
        # 检查一下音乐是否已加载
            try:
                pygame.mixer.music.play(loops)
            except pygame.error as e:
                if "not loaded" in str(e):
                    print("错误：尝试播放未加载的音乐。请检查load_audio中的路径。")
                else:
                    raise e


    def play_shoot(self):
        """播放子弹发射音效"""
        if self.sfx_on and self.shoot_sound:
            self.shoot_sound.play()

    def play_hit(self):
        """播放子弹击中音效"""
        if self.sfx_on and self.hit_sound:
            self.hit_sound.play()

    def play_crash(self):  
        """播放碰撞音效"""
        if self.sfx_on and self.crash_sound:
            self.crash_sound.play()

    