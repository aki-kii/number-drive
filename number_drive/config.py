"""
ゲームの設定値を定義するモジュール
"""
import pygame
from pathlib import Path

# 画面サイズ
SCREEN_WIDTH = 800  # ひと回り小さく
SCREEN_HEIGHT = 600  # ひと回り小さく

# フレームレート
FPS = 60

# 色の定義
BACKGROUND_COLOR = (5, 5, 20)  # より暗い背景色（ロゴと同じ）
MAIN_COLOR_PINK = (255, 0, 255)  # 鮮やかなネオンピンク
MAIN_COLOR_ORANGE = (255, 165, 0)  # オレンジ
MAIN_COLOR_YELLOW = (255, 255, 0)  # イエロー
ACCENT_COLOR = (0, 255, 255)  # シアン
POINT_COLOR = (148, 0, 211)  # ネオン紫
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BUTTON_INACTIVE = (17, 17, 17)  # 非選択ボタンの色
BUTTON_HOVER = (34, 34, 34)  # ホバー時のボタン色
BUTTON_BORDER = (102, 102, 102)  # ボタンの枠線
TEXT_GRAY = (204, 204, 204)  # テキストのグレー
FOOTER_GRAY = (136, 136, 136)  # フッターのグレー
DECORATION_COLOR = (0, 255, 255, 10)  # 装飾用の色（透明度を固定）

# ナンバープレートの色
PLATE_YELLOW = (255, 240, 0)  # 軽自動車・自家用/普通車・事業用の黄色
PLATE_WHITE = (255, 255, 255)  # 普通車・自家用の白色
PLATE_GREEN = (0, 180, 0)  # かけ算用の緑色

# フォントサイズ
TITLE_FONT_SIZE = 48  # タイトル用（少し小さく）
LARGE_FONT_SIZE = 36  # 大きめのテキスト用
MEDIUM_FONT_SIZE = 24  # 中くらいのテキスト用
SMALL_FONT_SIZE = 16  # 小さめのテキスト用（ピクセルフォントは大きく見えるので小さめに）

# ゲーム設定
TOTAL_QUESTIONS = 10  # 出題数

# アセットのパス
BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "images"
FONTS_DIR = BASE_DIR / "fonts"

# ロゴのパス
LOGO_PATH = IMAGES_DIR / "logo.png"
PIXEL_FONT_PATH = FONTS_DIR / "press_start_2p.ttf"

# フォントの読み込み
def get_font(size):
    """指定したサイズのフォントを取得する"""
    # サイズを整数に変換
    size = int(size)
    # ピクセルフォントを使用
    try:
        return pygame.font.Font(str(PIXEL_FONT_PATH), size)
    except Exception as e:
        print(f"Error loading font: {e}")
        # フォントが見つからない場合はデフォルトフォントを使用
        return pygame.font.SysFont("Arial", size)

# ナンバープレートの除外ルール
EXCLUDED_NUMBERS = [13, 42, 49]  # 下二桁に特定の番号がつく場合は除外
