"""
タイトル画面を定義するモジュール
"""
import pygame
from typing import List, Tuple

from number_drive.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TITLE_FONT_SIZE, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE,
    MAIN_COLOR_PINK, ACCENT_COLOR, WHITE, LOGO_PATH, get_font
)
from number_drive.game_enums import GameMode, GameState


class TitleScreen:
    """タイトル画面を表すクラス"""
    
    def __init__(self, game):
        """
        タイトル画面の初期化
        
        Args:
            game: ゲームのインスタンス
        """
        self.game = game
        self.selected_mode = 0  # 0: EASY, 1: NORMAL, 2: HARD
        
        # ロゴの読み込み
        try:
            self.logo = pygame.image.load(str(LOGO_PATH))
            logo_width = SCREEN_WIDTH * 0.8
            logo_height = logo_width * self.logo.get_height() / self.logo.get_width()
            self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
        except:
            self.logo = None
            print(f"Warning: Could not load logo from {LOGO_PATH}")
        
        # モード選択ボタンの位置とサイズ
        self.mode_buttons = [
            pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50),
            pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50),
            pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140, 200, 50)
        ]
    
    def handle_event(self, event):
        """
        イベント処理
        
        Args:
            event: Pygameのイベント
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_mode = (self.selected_mode - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selected_mode = (self.selected_mode + 1) % 3
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # 選択したモードを設定してゲーム準備画面へ
                self.game.set_game_mode(list(GameMode)[self.selected_mode])
                self.game.change_state(GameState.PREPARE)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                for i, button in enumerate(self.mode_buttons):
                    if button.collidepoint(event.pos):
                        self.selected_mode = i
                        self.game.set_game_mode(list(GameMode)[i])
                        self.game.change_state(GameState.PREPARE)
                        break
    
    def update(self):
        """画面の状態を更新する"""
        pass
    
    def render(self, screen):
        """
        画面を描画する
        
        Args:
            screen: 描画対象のサーフェス
        """
        # ロゴを描画
        if self.logo:
            logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(self.logo, logo_rect)
        else:
            # ロゴがない場合はテキストで代用
            title_font = get_font(TITLE_FONT_SIZE)
            title_text = title_font.render("NumberDrive!", True, MAIN_COLOR_PINK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(title_text, title_rect)
        
        # ゲームの説明
        desc_font = get_font(SMALL_FONT_SIZE)
        desc_text = desc_font.render("ナンバープレートの数字を使った計算ゲーム！", True, WHITE)
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(desc_text, desc_rect)
        
        # 難易度選択ボタン
        mode_names = ["イージーモード", "ノーマルモード", "ハードモード"]
        mode_descs = [
            "足し算のみ（軽自動車・自家用ナンバー）",
            "足し算と引き算（普通車・自家用ナンバー）",
            "足し算、引き算、掛け算（普通車・事業用ナンバー）"
        ]
        
        button_font = get_font(MEDIUM_FONT_SIZE)
        desc_font = get_font(SMALL_FONT_SIZE)
        
        for i, (button, name, desc) in enumerate(zip(self.mode_buttons, mode_names, mode_descs)):
            # ボタンの背景
            color = ACCENT_COLOR if i == self.selected_mode else (100, 100, 100)
            pygame.draw.rect(screen, color, button, border_radius=10)
            pygame.draw.rect(screen, WHITE, button, width=2, border_radius=10)
            
            # ボタンのテキスト
            text = button_font.render(name, True, WHITE)
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)
            
            # 説明テキスト
            desc_text = desc_font.render(desc, True, WHITE)
            desc_rect = desc_text.get_rect(center=(button.centerx, button.bottom + 20))
            screen.blit(desc_text, desc_rect)
        
        # 操作方法
        help_font = get_font(SMALL_FONT_SIZE)
        help_text1 = help_font.render("↑↓キー: 選択移動", True, WHITE)
        help_text2 = help_font.render("スペース/エンター: 決定", True, WHITE)
        
        help_rect1 = help_text1.get_rect(bottomleft=(20, SCREEN_HEIGHT - 40))
        help_rect2 = help_text2.get_rect(bottomleft=(20, SCREEN_HEIGHT - 10))
        
        screen.blit(help_text1, help_rect1)
        screen.blit(help_text2, help_rect2)
