"""
ゲーム準備画面を定義するモジュール
"""
import pygame
import time
from typing import Optional

from number_drive.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LARGE_FONT_SIZE, MEDIUM_FONT_SIZE,
    WHITE, ACCENT_COLOR, get_font
)
from number_drive.game_enums import GameState, GameMode


class PrepareScreen:
    """ゲーム準備画面を表すクラス"""
    
    def __init__(self, game):
        """
        ゲーム準備画面の初期化
        
        Args:
            game: ゲームのインスタンス
        """
        self.game = game
        self.countdown = 3  # カウントダウン秒数
        self.start_time = None
        self.waiting_for_start = True
    
    def reset(self):
        """画面の状態をリセットする"""
        self.countdown = 3
        self.start_time = None
        self.waiting_for_start = True
    
    def handle_event(self, event):
        """
        イベント処理
        
        Args:
            event: Pygameのイベント
        """
        if self.waiting_for_start and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.waiting_for_start = False
                self.start_time = time.time()
    
    def update(self):
        """画面の状態を更新する"""
        if not self.waiting_for_start and self.start_time:
            elapsed = time.time() - self.start_time
            self.countdown = 3 - int(elapsed)
            
            if self.countdown <= 0:
                # カウントダウン終了、ゲーム画面へ
                self.game.change_state(GameState.PLAYING)
    
    def render(self, screen):
        """
        画面を描画する
        
        Args:
            screen: 描画対象のサーフェス
        """
        # 選択した難易度の表示
        mode_names = ["イージーモード", "ノーマルモード", "ハードモード"]
        mode_index = list(GameMode).index(self.game.game_mode)
        
        mode_font = get_font(LARGE_FONT_SIZE)
        mode_text = mode_font.render(mode_names[mode_index], True, WHITE)
        mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(mode_text, mode_rect)
        
        if self.waiting_for_start:
            # スタート待ち
            prompt_font = get_font(MEDIUM_FONT_SIZE)
            prompt_text = prompt_font.render("スペースキーを押してスタート", True, ACCENT_COLOR)
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # 点滅効果
            if int(time.time() * 2) % 2 == 0:
                screen.blit(prompt_text, prompt_rect)
        else:
            # カウントダウン
            count_font = get_font(LARGE_FONT_SIZE * 2)
            count_text = count_font.render(str(max(1, self.countdown)), True, ACCENT_COLOR)
            count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(count_text, count_rect)
