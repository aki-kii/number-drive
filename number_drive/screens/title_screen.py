"""
タイトル画面を定義するモジュール
"""
import pygame
import random
from typing import List, Tuple
import os

from number_drive.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TITLE_FONT_SIZE, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE,
    MAIN_COLOR_PINK, ACCENT_COLOR, WHITE, BLACK, LOGO_PATH, BUTTON_INACTIVE, BUTTON_HOVER, BUTTON_BORDER, TEXT_GRAY, FOOTER_GRAY, DECORATION_COLOR, get_font,
    IMAGES_DIR
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
        
        # 画面の中央に合わせて配置するための計算
        # 要素間の間隔を設定（余白を若干増やす）
        self.element_spacing = SCREEN_HEIGHT * 0.03  # 要素間の基本間隔を増やす
        
        # ロゴの読み込み
        try:
            self.logo = pygame.image.load(str(LOGO_PATH))
            # 画面幅に対する相対的なサイズ設定
            logo_width = int(SCREEN_WIDTH * 0.45)  # 画面幅の45%
            logo_height = logo_width * self.logo.get_height() / self.logo.get_width()
            self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
        except:
            self.logo = None
            print(f"Warning: Could not load logo from {LOGO_PATH}")
        
        # ロゴの高さを計算
        logo_height = self.logo.get_height() if self.logo else TITLE_FONT_SIZE * 1.5
        
        # 説明文の高さ（推定）
        desc_height = SMALL_FONT_SIZE
        
        # ボタンの高さと間隔（余白を若干増やす）
        button_height = int(SCREEN_HEIGHT * 0.07)  # 画面高さの7%に戻す
        button_spacing = self.element_spacing * 0.8  # 間隔を増やす
        
        # 3つのボタンの合計高さ
        buttons_total_height = button_height * 3 + button_spacing * 2
        
        # フッターの高さ（推定）
        footer_height = SMALL_FONT_SIZE
        
        # 全体の高さを計算
        total_content_height = (
            logo_height +                  # ロゴ
            self.element_spacing * 1.2 +   # ロゴと説明文の間隔（増やす）
            desc_height +                  # 説明文
            self.element_spacing * 1.5 +   # 説明文とボタンの間隔（増やす）
            buttons_total_height +         # ボタン群
            self.element_spacing * 1.8 +   # ボタンとフッターの間隔（増やす）
            footer_height                  # フッター
        )
        
        # 全体を中央に配置するための開始位置
        start_y = (SCREEN_HEIGHT - total_content_height) / 2
        
        # 各要素の位置を計算
        self.logo_y_pos = start_y + logo_height / 2
        self.desc_y_pos = self.logo_y_pos + logo_height / 2 + self.element_spacing * 1.2 + desc_height / 2
        self.button_y_start = self.desc_y_pos + desc_height / 2 + self.element_spacing * 1.5
        self.button_spacing = button_spacing
        
        # モード選択ボタンの位置とサイズ（ボタンの余白を増やす）
        button_width = int(SCREEN_WIDTH * 0.4)  # 画面幅の40%に戻す
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.mode_buttons = [
            pygame.Rect(button_x, self.button_y_start, button_width, button_height),
            pygame.Rect(button_x, self.button_y_start + button_height + self.button_spacing, button_width, button_height),
            pygame.Rect(button_x, self.button_y_start + (button_height + self.button_spacing) * 2, button_width, button_height)
        ]
        
        # フッターの位置は最後のボタンの下端 + 間隔
        last_button = self.mode_buttons[-1]
        self.footer_y_pos = last_button.bottom + self.element_spacing * 1.8
        
        # ロゴの安全領域を定義（車がロゴに被らないようにする）
        logo_safe_margin = 20  # ロゴの周りに余裕を持たせる
        self.logo_safe_area = pygame.Rect(
            SCREEN_WIDTH // 2 - (logo_width // 2) - logo_safe_margin,
            self.logo_y_pos - (logo_height // 2) - logo_safe_margin,
            logo_width + (logo_safe_margin * 2),
            logo_height + (logo_safe_margin * 2)
        )
        
        # 車の画像を読み込む
        self.cars = []
        car_paths = [
            os.path.join(IMAGES_DIR, "cars", "add_car.png"),
            os.path.join(IMAGES_DIR, "cars", "subtruct_car.png"),
            os.path.join(IMAGES_DIR, "cars", "mulchply_car.png")
        ]
        
        for car_path in car_paths:
            try:
                car_img = pygame.image.load(car_path)
                # 車の画像サイズを調整（画面幅の15%程度）
                car_width = int(SCREEN_WIDTH * 0.15)
                car_height = car_width * car_img.get_height() / car_img.get_width()
                car_img = pygame.transform.scale(car_img, (car_width, car_height))
                self.cars.append(car_img)
            except Exception as e:
                print(f"Warning: Could not load car image from {car_path}: {e}")
        
        # 車の位置をランダムに設定（ロゴに被らないように）
        self.car_positions = []
        
        # 車の配置を試行
        for _ in range(3):  # 3台の車を配置
            max_attempts = 20  # 最大試行回数
            for attempt in range(max_attempts):
                # 画面内のランダムな位置
                x = random.uniform(SCREEN_WIDTH * 0.1, SCREEN_WIDTH * 0.9)
                y = random.uniform(SCREEN_HEIGHT * 0.1, SCREEN_HEIGHT * 0.9)
                
                # 車の大きさを考慮した矩形
                car_width = self.cars[0].get_width() if self.cars else 100
                car_height = self.cars[0].get_height() if self.cars else 50
                car_rect = pygame.Rect(x - car_width/2, y - car_height/2, car_width, car_height)
                
                # ロゴの安全領域と重ならないかチェック
                if not self.logo_safe_area.colliderect(car_rect):
                    # 他の車と重ならないかチェック
                    if not any(pygame.Rect(pos[0] - car_width/2, pos[1] - car_height/2, car_width, car_height).colliderect(car_rect) for pos in self.car_positions):
                        self.car_positions.append((x, y))
                        break
            
            # 配置できなかった場合は画面外に配置（描画されない）
            if len(self.car_positions) <= _:
                self.car_positions.append((-100, -100))
        
        # 車の回転角度をランダムに設定
        self.car_rotations = [random.randint(-20, 20) for _ in range(3)]
        
        # 車の反転状態をランダムに設定
        self.car_flips = [random.choice([True, False]) for _ in range(3)]
        
        # ホバー状態の追跡
        self.hovered_button = None
        
        # 装飾用の数字と記号（ランダムに配置）
        self.decorations = []
        symbols = ["+", "-", "×", "="]
        
        # 画面の安全領域を定義（重要な要素と重ならないエリア）
        # ロゴの高さを計算
        logo_height = self.logo.get_height() if self.logo else TITLE_FONT_SIZE * 1.5
        
        # 全体のコンテンツ領域を安全領域として設定
        content_top = self.logo_y_pos - logo_height/2 - 20
        content_bottom = self.footer_y_pos + 20
        content_height = content_bottom - content_top
        
        safe_areas = [
            # コンテンツ全体の領域
            pygame.Rect(SCREEN_WIDTH // 2 - int(SCREEN_WIDTH * 0.25), 
                      content_top, 
                      int(SCREEN_WIDTH * 0.5), 
                      content_height)
        ]
        
        # 車の画像の位置も安全領域に追加
        for i, pos in enumerate(self.car_positions):
            if i < len(self.cars) and self.cars[i]:
                car_width = self.cars[i].get_width()
                car_height = self.cars[i].get_height()
                # 車の周りに少し余裕を持たせる
                safe_areas.append(pygame.Rect(pos[0] - car_width/2 - 10, 
                                            pos[1] - car_height/2 - 10, 
                                            car_width + 20, 
                                            car_height + 20))
        
        # 装飾を配置（安全領域を避ける）
        for _ in range(12):  # 数を減らす
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
                # 選択したモードを設定
                self.game.game_mode = list(GameMode)[self.selected_mode]
                # 準備画面へ
                self.game.change_state(GameState.PREPARE)
        
        elif event.type == pygame.MOUSEMOTION:
            # マウスホバーの検出
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_button = None
            for i, button in enumerate(self.mode_buttons):
                if button.collidepoint(mouse_pos):
                    self.hovered_button = i
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # マウスクリックの検出
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.mode_buttons):
                if button.collidepoint(mouse_pos):
                    self.selected_mode = i
                    # 選択したモードを設定
                    self.game.game_mode = list(GameMode)[self.selected_mode]
                    # 準備画面へ
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
        # 装飾的な数字と記号を描画（背景）
        for symbol, x, y, size, alpha in self.decorations:
            symbol_font = get_font(size)
            symbol_surface = symbol_font.render(symbol, True, (*ACCENT_COLOR[:3], alpha))
            screen.blit(symbol_surface, (x, y))
        
        # 車の画像を描画
        for i, (pos, rotation, flip) in enumerate(zip(self.car_positions, self.car_rotations, self.car_flips)):
            if i < len(self.cars) and self.cars[i]:
                # 車の画像を回転・反転
                car_img = self.cars[i]
                if flip:
                    car_img = pygame.transform.flip(car_img, True, False)
                rotated_car = pygame.transform.rotate(car_img, rotation)
                # 回転後の画像の中心を元の位置に合わせる
                car_rect = rotated_car.get_rect(center=pos)
                screen.blit(rotated_car, car_rect)
        
        # ロゴを描画
        if self.logo:
            logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, self.logo_y_pos))
            screen.blit(self.logo, logo_rect)
        else:
            # ロゴがない場合はテキストで代用
            title_font = get_font(TITLE_FONT_SIZE)
            title_text = title_font.render("NumberDrive!", True, MAIN_COLOR_PINK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, self.logo_y_pos))
            screen.blit(title_text, title_rect)
        
        # ゲームの説明（シンプルに）
        desc_font = get_font(SMALL_FONT_SIZE - 4)  # フォントサイズを小さく
        desc_text = desc_font.render("Solve math problems with license plates!", True, MAIN_COLOR_PINK)
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, self.desc_y_pos))
        screen.blit(desc_text, desc_rect)
        
        # 難易度選択ボタン
        mode_names = ["Easy Mode", "Normal Mode", "Hard Mode"]
        mode_descs = [
            "Addition only",
            "Add & Subtract",
            "Add, Subtract & Multiply"
        ]
        
        # ボタン内のテキストサイズを調整
        button_font = get_font(SMALL_FONT_SIZE - 2)  # ボタンテキストも小さく
        desc_font = get_font(SMALL_FONT_SIZE - 4)
        
        for i, (button, name, desc) in enumerate(zip(self.mode_buttons, mode_names, mode_descs)):
            # ボタンの背景と選択状態に応じた色の設定
            if i == self.selected_mode:
                # 選択中のボタン
                color = ACCENT_COLOR
                text_color = BLACK
                border_color = ACCENT_COLOR
                
                # 選択されたボタンに光彩効果（より自然に）
                for j in range(3):
                    offset = (j + 1) * 5
                    alpha = 40 - j * 10
                    glow_surface = pygame.Surface((button.width + offset*2, button.height + offset*2), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, (*ACCENT_COLOR[:3], alpha), 
                                    (0, 0, button.width + offset*2, button.height + offset*2), border_radius=10)
                    screen.blit(glow_surface, (button.x - offset, button.y - offset))
            elif i == self.hovered_button:
                # ホバー中のボタン
                color = BUTTON_HOVER
                text_color = WHITE
                border_color = ACCENT_COLOR
            else:
                # 通常のボタン
                color = BUTTON_INACTIVE
                text_color = TEXT_GRAY
                border_color = BUTTON_BORDER
            
            # ボタンの描画（角丸長方形）
            pygame.draw.rect(screen, color, button, border_radius=10)
            pygame.draw.rect(screen, border_color, button, width=2, border_radius=10)
            
            # ボタン内のテキスト - 常に上下に配置して潰れないようにする
            name_text = button_font.render(name, True, text_color)
            desc_text = desc_font.render(desc, True, text_color)
            
            name_rect = name_text.get_rect(center=(button.centerx, button.centery - 12))
            desc_rect = desc_text.get_rect(center=(button.centerx, button.centery + 12))
            
            screen.blit(name_text, name_rect)
            screen.blit(desc_text, desc_rect)
        
        # 操作方法（画面下部中央に配置）
        help_font = get_font(SMALL_FONT_SIZE - 4)  # 小さめに
        help_text = help_font.render("↑↓: Select   Space/Enter: Confirm", True, FOOTER_GRAY)
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, self.footer_y_pos))
        screen.blit(help_text, help_rect)
