"""
ゲームのメインクラスと処理を定義するモジュール
"""
import pygame
import sys
import time
from typing import List, Tuple, Optional

from number_drive.game_enums import GameState, GameMode
from number_drive.screens.title_screen import TitleScreen
from number_drive.screens.game_screen import GameScreen
from number_drive.screens.result_screen import ResultScreen
from number_drive.screens.prepare_screen import PrepareScreen
from number_drive.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_COLOR, LOGO_PATH


class Game:
    """ゲームのメインクラス"""
    
    def __init__(self):
        """ゲームの初期化"""
        pygame.init()
        pygame.display.set_caption("NumberDrive!")
        
        # ウィンドウアイコンの設定（ロゴがあれば）
        try:
            icon = pygame.image.load(str(LOGO_PATH))
            pygame.display.set_icon(icon)
        except:
            pass
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.TITLE
        self.game_mode = GameMode.EASY
        
        # 各画面の初期化
        self.title_screen = TitleScreen(self)
        self.prepare_screen = PrepareScreen(self)
        self.game_screen = GameScreen(self)
        self.result_screen = ResultScreen(self)
        
        # ゲーム結果
        self.clear_time = 0.0
        self.best_times = {
            GameMode.EASY: float('inf'),
            GameMode.NORMAL: float('inf'),
            GameMode.HARD: float('inf')
        }
    
    def run(self):
        """ゲームのメインループ"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 現在の画面に応じたイベント処理
            if self.state == GameState.TITLE:
                self.title_screen.handle_event(event)
            elif self.state == GameState.PREPARE:
                self.prepare_screen.handle_event(event)
            elif self.state == GameState.PLAYING:
                self.game_screen.handle_event(event)
            elif self.state == GameState.RESULT:
                self.result_screen.handle_event(event)
    
    def update(self):
        """ゲーム状態の更新"""
        if self.state == GameState.TITLE:
            self.title_screen.update()
        elif self.state == GameState.PREPARE:
            self.prepare_screen.update()
        elif self.state == GameState.PLAYING:
            self.game_screen.update()
        elif self.state == GameState.RESULT:
            self.result_screen.update()
    
    def render(self):
        """画面の描画"""
        self.screen.fill(BACKGROUND_COLOR)
        
        if self.state == GameState.TITLE:
            self.title_screen.render(self.screen)
        elif self.state == GameState.PREPARE:
            self.prepare_screen.render(self.screen)
        elif self.state == GameState.PLAYING:
            self.game_screen.render(self.screen)
        elif self.state == GameState.RESULT:
            self.result_screen.render(self.screen)
        
        pygame.display.flip()
    
    def change_state(self, new_state: GameState):
        """ゲーム状態を変更する"""
        self.state = new_state
        
        # 状態変更時の初期化処理
        if new_state == GameState.PREPARE:
            self.prepare_screen.reset()
        elif new_state == GameState.PLAYING:
            self.game_screen.reset()
        elif new_state == GameState.RESULT:
            if self.clear_time < self.best_times[self.game_mode]:
                self.best_times[self.game_mode] = self.clear_time
    
    def set_game_mode(self, mode: GameMode):
        """ゲームモードを設定する"""
        self.game_mode = mode
    
    def set_clear_time(self, time: float):
        """クリアタイムを設定する"""
        self.clear_time = time
