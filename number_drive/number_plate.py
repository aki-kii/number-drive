"""
ナンバープレートの生成と描画を行うモジュール
"""
import random
import pygame
from enum import Enum, auto
from typing import Tuple

from number_drive.config import EXCLUDED_NUMBERS, PLATE_YELLOW, PLATE_WHITE, PLATE_GREEN, BLACK, WHITE


class OperationType(Enum):
    """演算子の種類を表す列挙型"""
    ADDITION = auto()      # 足し算
    SUBTRACTION = auto()   # 引き算
    MULTIPLICATION = auto()  # 掛け算


class NumberPlate:
    """ナンバープレートを表すクラス"""
    
    def __init__(self, operation_type: OperationType):
        """
        ナンバープレートの初期化
        
        Args:
            operation_type: 演算子の種類
        """
        self.operation_type = operation_type
        self.front_number, self.back_number = self._generate_valid_numbers()
        
        # 演算子に応じたプレートの色と文字色を設定
        if operation_type == OperationType.ADDITION:
            # 足し算：黄色地に黒文字
            self.plate_color = PLATE_YELLOW
            self.text_color = BLACK
        elif operation_type == OperationType.SUBTRACTION:
            # 引き算：白地に黒文字
            self.plate_color = PLATE_WHITE
            self.text_color = BLACK
        else:  # MULTIPLICATION
            # 掛け算：緑地に白文字
            self.plate_color = PLATE_GREEN
            self.text_color = WHITE
    
    def _generate_valid_numbers(self) -> Tuple[int, int]:
        """
        有効なナンバープレートの数字を生成する
        
        Returns:
            前半の数字と後半の数字のタプル
        """
        while True:
            # 前半は1〜99の範囲
            front = random.randint(1, 99)
            
            # 後半は00〜99の範囲
            back = random.randint(0, 99)
            
            # 除外ルールのチェック
            back_str = f"{back:02d}"
            if int(back_str) not in EXCLUDED_NUMBERS:
                return front, back
    
    def get_question(self) -> str:
        """
        問題文を取得する
        
        Returns:
            問題文（例: "12+34=?"）
        """
        if self.operation_type == OperationType.ADDITION:
            return f"{self.front_number}+{self.back_number:02d}=?"
        elif self.operation_type == OperationType.SUBTRACTION:
            return f"{self.front_number}-{self.back_number:02d}=?"
        else:  # MULTIPLICATION
            return f"{self.front_number}×{self.back_number:02d}=?"
    
    def get_answer(self) -> int:
        """
        正解を取得する
        
        Returns:
            計算結果
        """
        if self.operation_type == OperationType.ADDITION:
            return self.front_number + self.back_number
        elif self.operation_type == OperationType.SUBTRACTION:
            return self.front_number - self.back_number
        else:  # MULTIPLICATION
            return self.front_number * self.back_number
    
    def get_operation_name(self) -> str:
        """
        演算子の名前を取得する
        
        Returns:
            演算子の名前（例: "Addition"）
        """
        if self.operation_type == OperationType.ADDITION:
            return "Addition"
        elif self.operation_type == OperationType.SUBTRACTION:
            return "Subtraction"
        else:  # MULTIPLICATION
            return "Multiplication"
    
    def render(self, surface: pygame.Surface, x: int, y: int, width: int, height: int):
        """
        ナンバープレートを描画する
        
        Args:
            surface: 描画対象のサーフェス
            x: X座標
            y: Y座標
            width: 幅
            height: 高さ
        """
        # 画像のような比率に調整（横長のプレート）
        plate_width = width
        plate_height = int(width * 0.22)  # 画像の比率に合わせて高さを調整
        
        # 中央に配置するための調整
        plate_y = y + (height - plate_height) // 2
        
        # プレートの背景を描画
        plate_rect = pygame.Rect(x, plate_y, plate_width, plate_height)
        pygame.draw.rect(surface, self.plate_color, plate_rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, plate_rect, width=3, border_radius=10)
        
        # 数字を描画
        font_size = int(plate_height * 0.7)  # プレートの高さに対する比率
        font = pygame.font.SysFont("Arial", font_size)
        
        # 前半の数字
        front_text = font.render(f"{self.front_number}", True, self.text_color)
        front_rect = front_text.get_rect(center=(x + plate_width * 0.25, plate_y + plate_height // 2))
        surface.blit(front_text, front_rect)
        
        # 区切り線
        line_x = x + plate_width * 0.5
        pygame.draw.line(surface, self.text_color, 
                         (line_x, plate_y + plate_height * 0.2),
                         (line_x, plate_y + plate_height * 0.8), 3)
        
        # 後半の数字
        back_text = font.render(f"{self.back_number:02d}", True, self.text_color)
        back_rect = back_text.get_rect(center=(x + plate_width * 0.75, plate_y + plate_height // 2))
        surface.blit(back_text, back_rect)
