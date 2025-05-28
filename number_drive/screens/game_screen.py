"""
ゲーム画面を定義するモジュール
"""
import pygame
import time
import random
import os
from typing import List, Optional

from number_drive.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE, LARGE_FONT_SIZE,
    WHITE, ACCENT_COLOR, MAIN_COLOR_PINK, POINT_COLOR, BUTTON_INACTIVE, BUTTON_BORDER, 
    TOTAL_QUESTIONS, get_font, FOOTER_GRAY, IMAGES_DIR, BACKGROUND_COLOR, DECORATION_COLOR
)
from number_drive.number_plate import NumberPlate, OperationType
from number_drive.game_enums import GameState, GameMode


class GameScreen:
    """ゲーム画面を表すクラス"""
    
    def __init__(self, game):
        """
        ゲーム画面の初期化
        
        Args:
            game: ゲームのインスタンス
        """
        self.game = game
        self.start_time = None
        self.current_time = 0.0
        self.current_question = 0
        self.number_plates = []
        self.current_input = ""
        self.feedback = None  # None: なし, True: 正解, False: 不正解
        self.feedback_time = None
        
        # 装飾用の車の画像を読み込む（1台だけ）
        self.car = None
        try:
            car_path = os.path.join(IMAGES_DIR, "cars", "add_car.png")
            car_img = pygame.image.load(car_path)
            # 車の画像サイズを調整（画面幅の10%程度 - ゲーム画面では小さめに）
            car_width = int(SCREEN_WIDTH * 0.1)
            car_height = car_width * car_img.get_height() / car_img.get_width()
            self.car = pygame.transform.scale(car_img, (car_width, car_height))
        except Exception as e:
            print(f"Warning: Could not load car image: {e}")
        
        # 車の位置、回転、反転をランダムに設定
        self.car_position = (SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.85)  # 右下に配置
        self.car_rotation = random.randint(-15, 15)
        self.car_flip = random.choice([True, False])
        
        # 装飾用の数字と記号
        self.decorations = []
        symbols = ["+", "-", "×", "="]
        
        # 安全領域（重要な要素と重ならないエリア）
        safe_areas = [
            # 上部のタイマーと問題数表示エリア
            pygame.Rect(0, 0, SCREEN_WIDTH, 100),
            # 中央のナンバープレートと問題表示エリア
            pygame.Rect(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.25, 
                      SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.4),
            # 入力エリア
            pygame.Rect(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.6, 
                      SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.15),
            # フィードバックエリア
            pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.7, 
                      SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.1),
            # 下部の操作ヘルプエリア
            pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
        ]
        
        # 車の周りも安全領域に追加
        if self.car:
            car_width = self.car.get_width()
            car_height = self.car.get_height()
            safe_areas.append(pygame.Rect(
                self.car_position[0] - car_width/2 - 10,
                self.car_position[1] - car_height/2 - 10,
                car_width + 20,
                car_height + 20
            ))
        
        # 装飾を配置（安全領域を避ける）
        for _ in range(8):  # ゲーム画面では装飾を少なめに
            attempts = 0
            while attempts < 10:  # 最大10回試行
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 50)
                
                # 安全領域との衝突チェック
                if not any(area.collidepoint(x, y) for area in safe_areas):
                    symbol = random.choice(symbols) if random.random() > 0.7 else str(random.randint(0, 9))
                    size = random.randint(12, 20)  # サイズ範囲を調整
                    alpha = random.randint(5, 15)  # 透明度をさらに高く（色をかなり薄く）
                    self.decorations.append((symbol, x, y, size, alpha))
                    break
                
                attempts += 1
    
    def reset(self):
        """画面の状態をリセットする"""
        self.start_time = time.time()
        self.current_time = 0.0
        self.current_question = 0
        self.current_input = ""
        self.feedback = None
        self.feedback_time = None
        
        # 問題を生成
        self.generate_questions()
    
    def generate_questions(self):
        """ゲームモードに応じた問題を生成する"""
        self.number_plates = []
        
        for _ in range(TOTAL_QUESTIONS):
            if self.game.game_mode == GameMode.EASY:
                # イージーモード: 足し算のみ
                operation = OperationType.ADDITION
            
            elif self.game.game_mode == GameMode.NORMAL:
                # ノーマルモード: 足し算と引き算をランダムに出題（比率 1:1）
                operation = random.choice([OperationType.ADDITION, OperationType.SUBTRACTION])
            
            else:  # HARD
                # ハードモード: 足し算、引き算、掛け算をランダムに出題（比率 4:4:2）
                operation = random.choices(
                    [OperationType.ADDITION, OperationType.SUBTRACTION, OperationType.MULTIPLICATION],
                    weights=[4, 4, 2],
                    k=1
                )[0]
            
            self.number_plates.append(NumberPlate(operation))
    
    def handle_event(self, event):
        """
        イベント処理
        
        Args:
            event: Pygameのイベント
        """
        if event.type == pygame.KEYDOWN:
            if self.feedback is not None:
                # フィードバック表示中は何もしない
                return
                
            if event.key == pygame.K_BACKSPACE:
                # バックスペースで1文字削除
                self.current_input = self.current_input[:-1]
            
            elif event.key == pygame.K_RETURN:
                # エンターキーで回答を確定
                self.check_answer()
            
            elif event.unicode.isdigit() or (event.unicode == '-' and not self.current_input):
                # 数字または先頭のマイナス記号を入力
                self.current_input += event.unicode
    
    def check_answer(self):
        """回答をチェックする"""
        if not self.current_input:
            return
        
        try:
            user_answer = int(self.current_input)
            correct_answer = self.number_plates[self.current_question].get_answer()
            
            if user_answer == correct_answer:
                # 正解
                self.feedback = True
                self.feedback_time = time.time()
                
                # 次の問題へ進む準備
                self.current_question += 1
                self.current_input = ""
                
                # 全問題終了したらリザルト画面へ
                if self.current_question >= TOTAL_QUESTIONS:
                    self.game.set_clear_time(self.current_time)
                    self.game.change_state(GameState.RESULT)
            else:
                # 不正解
                self.feedback = False
                self.feedback_time = time.time()
        except ValueError:
            # 入力が数値でない場合
            self.feedback = False
            self.feedback_time = time.time()
    
    def update(self):
        """画面の状態を更新する"""
        # 経過時間を更新
        if self.start_time:
            self.current_time = time.time() - self.start_time
        
        # フィードバック表示の更新
        if self.feedback is not None and self.feedback_time:
            if time.time() - self.feedback_time > 0.5:  # 0.5秒間表示
                self.feedback = None
                self.feedback_time = None
    
    def render(self, screen):
        """
        画面を描画する
        
        Args:
            screen: 描画対象のサーフェス
        """
        if self.current_question >= TOTAL_QUESTIONS:
            return
        
        # 装飾的な数字と記号を描画（背景）
        for symbol, x, y, size, alpha in self.decorations:
            symbol_font = get_font(size)
            symbol_surface = symbol_font.render(symbol, True, (*ACCENT_COLOR[:3], alpha))
            screen.blit(symbol_surface, (x, y))
        
        # 車の画像を描画（背景として）
        if self.car:
            # 車を反転させる（必要な場合）
            if self.car_flip:
                car = pygame.transform.flip(self.car, True, False)
            else:
                car = self.car
            
            # 車を回転させる
            rotated_car = pygame.transform.rotate(car, self.car_rotation)
            
            # 回転後の画像の中心位置を調整
            car_rect = rotated_car.get_rect(center=self.car_position)
            
            # 車を描画
            screen.blit(rotated_car, car_rect)
        
        # 上部の装飾ライン
        pygame.draw.line(screen, ACCENT_COLOR, 
                        (SCREEN_WIDTH * 0.1, 60),
                        (SCREEN_WIDTH * 0.9, 60), 2)
        
        # タイマー表示
        timer_font = get_font(MEDIUM_FONT_SIZE)
        timer_text = timer_font.render(f"Time: {self.current_time:.1f}", True, WHITE)
        timer_rect = timer_text.get_rect(topleft=(30, 20))
        screen.blit(timer_text, timer_rect)
        
        # 問題数表示
        question_font = get_font(MEDIUM_FONT_SIZE)
        question_text = question_font.render(f"Q: {self.current_question + 1}/{TOTAL_QUESTIONS}", True, WHITE)
        question_rect = question_text.get_rect(topright=(SCREEN_WIDTH - 30, 20))
        screen.blit(question_text, question_rect)
        
        # ナンバープレート表示
        plate_width = SCREEN_WIDTH * 0.6
        plate_height = plate_width * 0.2
        plate_x = (SCREEN_WIDTH - plate_width) // 2
        plate_y = SCREEN_HEIGHT // 3
        
        # 演算子の種類表示（ナンバープレートの直上に配置）- 記号を追加
        current_plate = self.number_plates[self.current_question]
        op_name = current_plate.get_operation_name()
        op_symbol = ""
        
        # 演算子に対応する記号を追加
        if current_plate.operation_type == OperationType.ADDITION:
            op_symbol = "+"
        elif current_plate.operation_type == OperationType.SUBTRACTION:
            op_symbol = "-"
        elif current_plate.operation_type == OperationType.MULTIPLICATION:
            op_symbol = "×"
        
        op_font = get_font(MEDIUM_FONT_SIZE)
        op_text = op_font.render(f"{op_name} ({op_symbol})", True, ACCENT_COLOR)
        op_rect = op_text.get_rect(center=(SCREEN_WIDTH // 2, plate_y - 30))  # プレートの上に配置
        screen.blit(op_text, op_rect)
        
        # ナンバープレートの背景に光彩効果
        glow_surface = pygame.Surface((plate_width + 20, plate_height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*ACCENT_COLOR[:3], 100), 
                        (0, 0, plate_width + 20, plate_height + 20), border_radius=15)
        screen.blit(glow_surface, (plate_x - 10, plate_y - 10))
        
        current_plate.render(screen, plate_x, plate_y, plate_width, plate_height)
        
        # 入力エリア
        input_font = get_font(LARGE_FONT_SIZE)
        input_text = input_font.render(self.current_input or "_", True, MAIN_COLOR_PINK)
        input_rect = input_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3 + 10))  # 少し下に移動
        
        # 入力エリアの背景
        input_bg_rect = pygame.Rect(0, 0, max(input_rect.width + 40, 80), input_rect.height + 20)
        input_bg_rect.center = input_rect.center
        pygame.draw.rect(screen, BUTTON_INACTIVE, input_bg_rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_BORDER, input_bg_rect, width=2, border_radius=10)
        
        screen.blit(input_text, input_rect)
        
        # 入力ラベル表示（入力エリアの上に配置、被らないように）
        input_label_font = get_font(SMALL_FONT_SIZE)
        input_label_text = input_label_font.render("Input", True, MAIN_COLOR_PINK)
        input_label_rect = input_label_text.get_rect(center=(SCREEN_WIDTH // 2, input_bg_rect.top - 15))  # 入力エリアの上端から15px上
        screen.blit(input_label_text, input_label_rect)
        
        # フィードバック表示
        if self.feedback is not None:
            feedback_font = get_font(LARGE_FONT_SIZE * 1.5)
            if self.feedback:
                feedback_text = feedback_font.render("O", True, (0, 255, 0))  # 英語の「O」に変更
            else:
                feedback_text = feedback_font.render("X", True, (255, 0, 0))  # 英語の「X」に変更
            
            feedback_rect = feedback_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
            screen.blit(feedback_text, feedback_rect)
        
        # 下部の装飾ライン
        pygame.draw.line(screen, ACCENT_COLOR, 
                        (SCREEN_WIDTH * 0.1, SCREEN_HEIGHT - 60),
                        (SCREEN_WIDTH * 0.9, SCREEN_HEIGHT - 60), 2)
        
        # 操作ヘルプ（スタート画面と同じスタイル）
        help_font = get_font(SMALL_FONT_SIZE - 4)
        help_text = help_font.render("Number Keys: Input  Backspace: Delete  Enter: Confirm", True, FOOTER_GRAY)
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(help_text, help_rect)
