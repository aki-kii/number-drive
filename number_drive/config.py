"""
ゲームの設定値を定義するモジュール
"""
import pygame
from pathlib import Path

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# フレームレート
FPS = 60

# 色の定義
BACKGROUND_COLOR = (10, 10, 30)  # 濃い紺/黒
MAIN_COLOR_PINK = (255, 105, 180)  # ピンク
MAIN_COLOR_ORANGE = (255, 165, 0)  # オレンジ
MAIN_COLOR_YELLOW = (255, 255, 0)  # イエロー
ACCENT_COLOR = (0, 255, 255)  # ネオン風の水色/ミント
POINT_COLOR = (148, 0, 211)  # ネオン紫
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

# ナンバープレートの色
PLATE_YELLOW = (255, 240, 0)  # 軽自動車・自家用/普通車・事業用の黄色
PLATE_WHITE = (255, 255, 255)  # 普通車・自家用の白色

# フォントサイズ
TITLE_FONT_SIZE = 64
LARGE_FONT_SIZE = 48
MEDIUM_FONT_SIZE = 36
SMALL_FONT_SIZE = 24

# ゲーム設定
TOTAL_QUESTIONS = 10  # 出題数

# アセットのパス
BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "images"
FONTS_DIR = BASE_DIR / "fonts"

# ロゴのパス
LOGO_PATH = IMAGES_DIR / "logo.png"

# フォントの読み込み
def get_font(size):
    """指定したサイズのフォントを取得する"""
    # サイズを整数に変換
    size = int(size)
    # フォントが存在する場合はそれを使用、なければデフォルトフォントを使用
    try:
        return pygame.font.Font(str(FONTS_DIR / "main_font.ttf"), size)
    except:
        return pygame.font.SysFont("Arial", size)

# ナンバープレートの除外ルール
EXCLUDED_NUMBERS = [13, 42, 49]  # 下二桁に特定の番号がつく場合は除外
