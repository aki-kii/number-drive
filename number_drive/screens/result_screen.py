"""
結果画面を定義するモジュール
"""
import pygame
from typing import List, Tuple

from number_drive.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LARGE_FONT_SIZE, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE,
    WHITE, ACCENT_COLOR, MAIN_COLOR_PINK, POINT_COLOR, get_font
)
from number_drive.game_enums import GameState, GameMode


class ResultScreen:
    """結果画面を表すクラス"""
    
    def __init__(self, game):
        """
        結果画面の初期化
        
        Args:
            game: ゲームのインスタンス
        """
        self.game = game
        
        # ボタンの位置とサイズ
        button_width = 300
        button_height = 60
        button_y = SCREEN_HEIGHT * 3 // 4
        
        self.retry_button = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width - 20,
            button_y,
            button_width,
            button_height
        )
        
        self.change_mode_button = pygame.Rect(
            SCREEN_WIDTH // 2 + 20,
            button_y,
            button_width,
            button_height
        )
        
        self.selected_button = 0  # 0: リトライ, 1: モード変更
    
    def handle_event(self, event):
        """
        イベント処理
        
        Args:
            event: Pygameのイベント
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # 左右キーでボタン選択を切り替え
                self.selected_button = 1 - self.selected_button
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # 選択したボタンの処理を実行
                if self.selected_button == 0:
                    # リトライ
                    self.game.change_state(GameState.PREPARE)
                else:
                    # モード変更
                    self.game.change_state(GameState.TITLE)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                if self.retry_button.collidepoint(event.pos):
                    # リトライ
                    self.game.change_state(GameState.PREPARE)
                elif self.change_mode_button.collidepoint(event.pos):
                    # モード変更
                    self.game.change_state(GameState.TITLE)
    
    def update(self):
        """画面の状態を更新する"""
        pass
    
    def render(self, screen):
        """
        画面を描画する
        
        Args:
            screen: 描画対象のサーフェス
        """
        # 結果タイトル
        title_font = get_font(LARGE_FONT_SIZE)
        title_text = title_font.render("ゲームクリア！", True, MAIN_COLOR_PINK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # クリアタイム
        time_font = get_font(LARGE_FONT_SIZE)
        time_text = time_font.render(f"クリアタイム: {self.game.clear_time:.1f}秒", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(time_text, time_rect)
        
        # ベストタイム
        mode_index = list(GameMode).index(self.game.game_mode)
        mode_names = ["イージー", "ノーマル", "ハード"]
        best_time = self.game.best_times[self.game.game_mode]
        
        if best_time < float('inf'):
            best_font = get_font(MEDIUM_FONT_SIZE)
            best_text = best_font.render(f"{mode_names[mode_index]}モード ベストタイム: {best_time:.1f}秒", True, ACCENT_COLOR)
            best_rect = best_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(best_text, best_rect)
        
        # 新記録表示
        if self.game.clear_time == best_time:
            record_font = get_font(MEDIUM_FONT_SIZE)
            record_text = record_font.render("新記録達成！", True, POINT_COLOR)
            record_rect = record_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            screen.blit(record_text, record_rect)
        
        # ボタン描画
        button_font = get_font(MEDIUM_FONT_SIZE)
        
        # リトライボタン
        retry_color = ACCENT_COLOR if self.selected_button == 0 else (100, 100, 100)
        pygame.draw.rect(screen, retry_color, self.retry_button, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.retry_button, width=2, border_radius=10)
        
        retry_text = button_font.render("もう一度プレイ", True, WHITE)
        retry_text_rect = retry_text.get_rect(center=self.retry_button.center)
        screen.blit(retry_text, retry_text_rect)
        
        # モード変更ボタン
        change_color = ACCENT_COLOR if self.selected_button == 1 else (100, 100, 100)
        pygame.draw.rect(screen, change_color, self.change_mode_button, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.change_mode_button, width=2, border_radius=10)
        
        change_text = button_font.render("難易度変更", True, WHITE)
        change_text_rect = change_text.get_rect(center=self.change_mode_button.center)
        screen.blit(change_text, change_text_rect)
        
        # 操作ヘルプ
        help_font = get_font(SMALL_FONT_SIZE)
        help_text = help_font.render("←→キー: 選択移動  スペース/エンター: 決定", True, WHITE)
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(help_text, help_rect)
