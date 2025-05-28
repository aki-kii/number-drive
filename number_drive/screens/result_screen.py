"""
結果画面を定義するモジュール
"""
import pygame
import time
import random
import os
from typing import List, Tuple

from number_drive.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LARGE_FONT_SIZE, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE,
    WHITE, ACCENT_COLOR, MAIN_COLOR_PINK, POINT_COLOR, BUTTON_INACTIVE, BUTTON_BORDER, 
    FOOTER_GRAY, IMAGES_DIR, DECORATION_COLOR, get_font
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
        
        # 装飾用の車の画像を読み込む（2台）
        self.cars = []
        try:
            car_paths = [
                os.path.join(IMAGES_DIR, "cars", "add_car.png"),
                os.path.join(IMAGES_DIR, "cars", "subtruct_car.png")
            ]
            
            for car_path in car_paths:
                car_img = pygame.image.load(car_path)
                # 車の画像サイズを調整（画面幅の15%程度）
                car_width = int(SCREEN_WIDTH * 0.15)
                car_height = car_width * car_img.get_height() / car_img.get_width()
                self.cars.append(pygame.transform.scale(car_img, (car_width, car_height)))
        except Exception as e:
            print(f"Warning: Could not load car image: {e}")
        
        # 車の位置、回転、反転をランダムに設定
        self.car_positions = [
            (SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.7),  # 左下
            (SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.7)   # 右下
        ]
        self.car_rotations = [random.randint(-20, 20) for _ in range(2)]
        self.car_flips = [random.choice([True, False]) for _ in range(2)]
        
        # 装飾用の数字と記号
        self.decorations = []
        symbols = ["+", "-", "×", "="]
        
        # 要素間の間隔を設定
        self.element_spacing = SCREEN_HEIGHT * 0.03
        
        # ボタンの位置とサイズ（相対的に配置）- 縦に並べる
        button_width = int(SCREEN_WIDTH * 0.45)  # 画面幅の45%に拡大（余白を増やす）
        button_height = int(SCREEN_HEIGHT * 0.08)  # 画面高さの8%に拡大（余白を増やす）
        button_spacing = button_height * 0.5  # ボタン間の間隔
        
        # 1つ目のボタン（Play Again）
        self.retry_button = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            SCREEN_HEIGHT * 0.6,
            button_width,
            button_height
        )
        
        # 2つ目のボタン（Change Difficulty）
        self.change_mode_button = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            self.retry_button.bottom + button_spacing,
            button_width,
            button_height
        )
        
        self.selected_button = 0  # 0: リトライ, 1: モード変更
        self.hovered_button = None  # マウスホバー用
        
        # 安全領域（重要な要素と重ならないエリア）
        safe_areas = [
            # タイトル周辺
            pygame.Rect(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.15, 
                      SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.2),
            # クリアタイム表示周辺
            pygame.Rect(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.4, 
                      SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.1),
            # ボタン周辺（縦に並んだボタンに合わせて調整）
            pygame.Rect(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.55, 
                      SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.25),
            # 下部の操作ヘルプエリア
            pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
        ]
        
        # 車の周りも安全領域に追加
        for i, pos in enumerate(self.car_positions):
            if i < len(self.cars) and self.cars[i]:
                car_width = self.cars[i].get_width()
                car_height = self.cars[i].get_height()
                safe_areas.append(pygame.Rect(
                    pos[0] - car_width/2 - 10,
                    pos[1] - car_height/2 - 10,
                    car_width + 20,
                    car_height + 20
                ))
        
        # 装飾を配置（安全領域を避ける）
        for _ in range(12):
            attempts = 0
            while attempts < 10:  # 最大10回試行
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 50)
                
                # 安全領域との衝突チェック
                if not any(area.collidepoint(x, y) for area in safe_areas):
                    symbol = random.choice(symbols) if random.random() > 0.7 else str(random.randint(0, 9))
                    size = random.randint(12, 24)
                    alpha = random.randint(5, 15)  # 透明度をさらに高く（色をかなり薄く）
                    self.decorations.append((symbol, x, y, size, alpha))
                    break
                
                attempts += 1
    
    def handle_event(self, event):
        """
        イベント処理
        
        Args:
            event: Pygameのイベント
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # 上下キーでボタン選択を切り替え
                self.selected_button = 1 - self.selected_button
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # 選択したボタンの処理を実行
                if self.selected_button == 0:
                    # リトライ
                    self.game.change_state(GameState.PREPARE)
                else:
                    # モード変更
                    self.game.change_state(GameState.TITLE)
        
        elif event.type == pygame.MOUSEMOTION:
            # マウスホバーの検出
            self.hovered_button = None
            if self.retry_button.collidepoint(event.pos):
                self.hovered_button = 0
            elif self.change_mode_button.collidepoint(event.pos):
                self.hovered_button = 1
        
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
        # 装飾的な数字と記号を描画（背景）
        for symbol, x, y, size, alpha in self.decorations:
            symbol_font = get_font(size)
            symbol_surface = symbol_font.render(symbol, True, DECORATION_COLOR)
            screen.blit(symbol_surface, (x, y))
        
        # 車の画像を描画（背景として）
        for i, car in enumerate(self.cars):
            if car and i < len(self.car_positions):
                # 車を反転させる（必要な場合）
                if self.car_flips[i]:
                    car = pygame.transform.flip(car, True, False)
                
                # 車を回転させる
                rotated_car = pygame.transform.rotate(car, self.car_rotations[i])
                
                # 回転後の画像の中心位置を調整
                car_rect = rotated_car.get_rect(center=self.car_positions[i])
                
                # 車を描画
                screen.blit(rotated_car, car_rect)
        
        # 上部の装飾ライン
        pygame.draw.line(screen, ACCENT_COLOR, 
                        (SCREEN_WIDTH * 0.1, 60),
                        (SCREEN_WIDTH * 0.9, 60), 2)
        
        # 結果タイトル
        title_font = get_font(LARGE_FONT_SIZE)
        title_text = title_font.render("Game Clear!", True, MAIN_COLOR_PINK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.25))
        
        # タイトルの背景に光彩効果
        for j in range(3):
            offset = (j + 1) * 5
            alpha = 40 - j * 10
            glow_surface = pygame.Surface((title_rect.width + offset*2, title_rect.height + offset*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*MAIN_COLOR_PINK[:3], alpha), 
                            (0, 0, title_rect.width + offset*2, title_rect.height + offset*2), border_radius=10)
            screen.blit(glow_surface, (title_rect.x - offset, title_rect.y - offset))
        
        screen.blit(title_text, title_rect)
        
        # クリアしたモードを表示
        mode_names = {
            GameMode.EASY: "Easy Mode",
            GameMode.NORMAL: "Normal Mode",
            GameMode.HARD: "Hard Mode"
        }
        mode_font = get_font(MEDIUM_FONT_SIZE)
        mode_text = mode_font.render(f"Cleared: {mode_names[self.game.game_mode]}", True, ACCENT_COLOR)
        mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.38))
        screen.blit(mode_text, mode_rect)
        
        # クリアタイム
        time_font = get_font(LARGE_FONT_SIZE)
        time_text = time_font.render(f"Clear Time: {self.game.clear_time:.1f} sec", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.48))
        screen.blit(time_text, time_rect)
        
        # ボタン描画
        button_font = get_font(MEDIUM_FONT_SIZE - 4)
        
        # リトライボタン
        retry_color = ACCENT_COLOR if self.selected_button == 0 else BUTTON_INACTIVE
        if self.hovered_button == 0:
            retry_color = BUTTON_INACTIVE
            border_color = ACCENT_COLOR
        else:
            border_color = BUTTON_BORDER
        
        pygame.draw.rect(screen, retry_color, self.retry_button, border_radius=10)
        pygame.draw.rect(screen, border_color, self.retry_button, width=2, border_radius=10)
        
        # ボタンテキストに余白を追加（テキストを小さくする）
        retry_text = button_font.render("Play Again", True, WHITE)
        retry_text_rect = retry_text.get_rect(center=self.retry_button.center)
        screen.blit(retry_text, retry_text_rect)
        
        # モード変更ボタン
        change_color = ACCENT_COLOR if self.selected_button == 1 else BUTTON_INACTIVE
        if self.hovered_button == 1:
            change_color = BUTTON_INACTIVE
            border_color = ACCENT_COLOR
        else:
            border_color = BUTTON_BORDER
        
        pygame.draw.rect(screen, change_color, self.change_mode_button, border_radius=10)
        pygame.draw.rect(screen, border_color, self.change_mode_button, width=2, border_radius=10)
        
        # ボタンテキストに余白を追加（テキストを小さくする）
        change_text = button_font.render("Change Difficulty", True, WHITE)
        change_text_rect = change_text.get_rect(center=self.change_mode_button.center)
        screen.blit(change_text, change_text_rect)
        
        # 下部の装飾ライン
        pygame.draw.line(screen, ACCENT_COLOR, 
                        (SCREEN_WIDTH * 0.1, SCREEN_HEIGHT - 60),
                        (SCREEN_WIDTH * 0.9, SCREEN_HEIGHT - 60), 2)
        
        # 操作ヘルプ（上下キーに変更）
        help_font = get_font(SMALL_FONT_SIZE - 4)
        help_text = help_font.render("↑↓: Select   Space/Enter: Confirm", True, FOOTER_GRAY)
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(help_text, help_rect)
