class GameStats:
    """游戏状态管理类：跟踪游戏分数、生命、等级等状态"""
    
    def __init__(self, ai_game):
        """初始化游戏统计信息"""
        self.settings = ai_game.settings  # 引用游戏配置参数
        self.reset_stats()                # 重置游戏进行中的统计数据
        self.game_active = False          # 游戏活动状态（默认未激活）
        self.high_score = 0               # 历史最高分（永久保存）
        self.level = 1                    # 游戏当前等级（初始为1）

    def reset_stats(self):
        """重置游戏进行中的动态统计数据（不影响最高分）"""
        self.ships_left = self.settings.ship_limit  # 剩余飞船数量（从配置获取）
        self.score = 0                             # 当前分数（重置为0）
        self.level = 1                             # 当前等级（重置为1）