#!/usr/bin/env python3
"""
NumberDrive! - ナンバープレートの数字を使った計算ゲーム
"""
import sys
import pygame
from number_drive.game import Game


def main():
    """メイン関数"""
    # Pygameの初期化
    pygame.init()
    
    # ゲームの作成と実行
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
