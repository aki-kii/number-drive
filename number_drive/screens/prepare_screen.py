"""
ゲーム準備画面を定義するモジュール
"""
import pygame
import time
import random
from typing import Optional

from number_drive.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LARGE_FONT_SIZE, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE,
    WHITE, ACCENT_COLOR, MAIN_COLOR_PINK, BUTTON_INACTIVE, BUTTON_BORDER, TEXT_GRAY, FOOTER_GRAY, DECORATION_COLOR, get_font
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
        
        # 装飾用の数字と記号（ランダムに配置）
        self.decorations = []
        symbols = ["+", "-", "×", "="]
        
        # 画面の安全領域を定義（重要な要素と重ならないエリア）
        mode_y = SCREEN_HEIGHT * 0.22  # モード名の位置
        prompt_y = SCREEN_HEIGHT * 0.45  # プロンプトの位置
        
        safe_areas = [
            # モード名周辺
            pygame.Rect(SCREEN_WIDTH // 2 - 300, mode_y - 50, 600, 100),
            # プロンプト周辺
            pygame.Rect(SCREEN_WIDTH // 2 - 200, prompt_y - 50, 400, 200),
            # フッター周辺
            pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
        ]
        
        # 装飾を配置（安全領域を避ける）
        for _ in range(15):
            attempts = 0
            while attempts < 10:  # 最大10回試行
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 50)
                
                # 安全領域との衝突チェック
                if not any(area.collidepoint(x, y) for area in safe_areas):
                    symbol = random.choice(symbols) if random.random() > 0.7 else str(random.randint(0, 9))
                    size = random.randint(12, 24)  # サイズ範囲を調整
                    alpha = random.randint(5, 15)  # 透明度をさらに高く（色をかなり薄く）
                    self.decorations.append((symbol, x, y, size, alpha))
                    break
                
                attempts += 1
    
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
            elif event.key == pygame.K_ESCAPE:
                # Escキーでタイトル画面に戻る
                self.game.change_state(GameState.TITLE)
    
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
        # 装飾的な数字と記号を描画（背景）
        for symbol, x, y, size, alpha in self.decorations:
            symbol_font = get_font(size)
            symbol_surface = symbol_font.render(symbol, True, (*ACCENT_COLOR[:3], alpha))
            screen.blit(symbol_surface, (x, y))
        
        # 選択した難易度の表示
        mode_names = ["Easy Mode", "Normal Mode", "Hard Mode"]
        mode_index = list(GameMode).index(self.game.game_mode)
        
        mode_font = get_font(LARGE_FONT_SIZE)
        mode_text = mode_font.render(mode_names[mode_index], True, MAIN_COLOR_PINK)
        mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.22))
        screen.blit(mode_text, mode_rect)
        
        if self.waiting_for_start:
            # スタート待ち
            prompt_font = get_font(MEDIUM_FONT_SIZE)
            prompt_text = prompt_font.render("Press Space to Start", True, ACCENT_COLOR)
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.45))
            
            # 点滅効果
            if int(time.time() * 2) % 2 == 0:
                screen.blit(prompt_text, prompt_rect)
        else:
            # カウントダウン（丸枠なし）
            count_font = get_font(LARGE_FONT_SIZE * 2)
            count_text = count_font.render(str(max(1, self.countdown)), True, ACCENT_COLOR)
            count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.45))
            
            # カウントダウン数字を描画（丸枠なし）
            screen.blit(count_text, count_rect)
        
        # 操作方法（画面下部中央に配置）
        if self.waiting_for_start:
            help_font = get_font(SMALL_FONT_SIZE - 4)
            help_text = help_font.render("Space/Enter: Start   Esc: Back to Title", True, FOOTER_GRAY)
            help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            screen.blit(help_text, help_rect)
