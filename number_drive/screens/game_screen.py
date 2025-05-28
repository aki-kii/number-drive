"""
ゲーム画面を定義するモジュール
"""
import pygame
import time
import random
from typing import List, Optional

from number_drive.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE, LARGE_FONT_SIZE,
    WHITE, ACCENT_COLOR, MAIN_COLOR_PINK, POINT_COLOR, TOTAL_QUESTIONS, get_font
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
        
        # タイマー表示
        timer_font = get_font(MEDIUM_FONT_SIZE)
        timer_text = timer_font.render(f"Time: {self.current_time:.1f}", True, WHITE)
        timer_rect = timer_text.get_rect(topleft=(20, 20))
        screen.blit(timer_text, timer_rect)
        
        # 問題数表示
        question_font = get_font(MEDIUM_FONT_SIZE)
        question_text = question_font.render(f"問題: {self.current_question + 1}/{TOTAL_QUESTIONS}", True, WHITE)
        question_rect = question_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(question_text, question_rect)
        
        # 演算子の種類表示
        current_plate = self.number_plates[self.current_question]
        op_font = get_font(MEDIUM_FONT_SIZE)
        op_text = op_font.render(current_plate.get_operation_name(), True, ACCENT_COLOR)
        op_rect = op_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(op_text, op_rect)
        
        # ナンバープレート表示
        plate_width = SCREEN_WIDTH * 0.7
        plate_height = plate_width * 0.2
        plate_x = (SCREEN_WIDTH - plate_width) // 2
        plate_y = SCREEN_HEIGHT // 3
        
        current_plate.render(screen, plate_x, plate_y, plate_width, plate_height)
        
        # 問題テキスト表示
        question_font = get_font(LARGE_FONT_SIZE)
        question_text = question_font.render(current_plate.get_question(), True, WHITE)
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, plate_y + plate_height + 60))
        screen.blit(question_text, question_rect)
        
        # 入力エリア
        input_font = get_font(LARGE_FONT_SIZE)
        input_text = input_font.render(self.current_input or "_", True, MAIN_COLOR_PINK)
        input_rect = input_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        screen.blit(input_text, input_rect)
        
        # フィードバック表示
        if self.feedback is not None:
            feedback_font = get_font(LARGE_FONT_SIZE * 1.5)
            if self.feedback:
                feedback_text = feedback_font.render("◯", True, (0, 255, 0))
            else:
                feedback_text = feedback_font.render("×", True, (255, 0, 0))
            
            feedback_rect = feedback_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
            screen.blit(feedback_text, feedback_rect)
        
        # 操作ヘルプ
        help_font = get_font(SMALL_FONT_SIZE)
        help_text = help_font.render("数字キー: 入力  バックスペース: 消去  エンター: 決定", True, WHITE)
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(help_text, help_rect)
