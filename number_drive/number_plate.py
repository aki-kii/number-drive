"""
ナンバープレートの生成と描画を行うモジュール
"""
import random
import pygame
from enum import Enum, auto
from typing import Tuple

from number_drive.config import EXCLUDED_NUMBERS, PLATE_YELLOW, PLATE_WHITE, BLACK, GREEN


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
            # 軽自動車・自家用：黄色地に黒文字
            self.plate_color = PLATE_YELLOW
            self.text_color = BLACK
        elif operation_type == OperationType.SUBTRACTION:
            # 普通車・自家用：白地に緑文字
            self.plate_color = PLATE_WHITE
            self.text_color = GREEN
        else:  # MULTIPLICATION
            # 普通車・事業用：黄色地に黒文字
            self.plate_color = PLATE_YELLOW
            self.text_color = BLACK
    
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
            演算子の名前（例: "足し算"）
        """
        if self.operation_type == OperationType.ADDITION:
            return "足し算"
        elif self.operation_type == OperationType.SUBTRACTION:
            return "引き算"
        else:  # MULTIPLICATION
            return "かけ算"
    
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
        # プレートの背景を描画
        plate_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, self.plate_color, plate_rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, plate_rect, width=3, border_radius=10)
        
        # 数字を描画
        font = pygame.font.SysFont("Arial", int(height // 2))
        
        # 前半の数字
        front_text = font.render(f"{self.front_number}", True, self.text_color)
        front_rect = front_text.get_rect(center=(x + width // 4, y + height // 2))
        surface.blit(front_text, front_rect)
        
        # 区切り線
        pygame.draw.line(surface, self.text_color, 
                         (x + width // 2 - 10, y + height // 4),
                         (x + width // 2 - 10, y + height * 3 // 4), 3)
        
        # 後半の数字
        back_text = font.render(f"{self.back_number:02d}", True, self.text_color)
        back_rect = back_text.get_rect(center=(x + width * 3 // 4, y + height // 2))
        surface.blit(back_text, back_rect)
