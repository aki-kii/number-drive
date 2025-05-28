"""
ゲームの列挙型を定義するモジュール
"""
from enum import Enum, auto


class GameState(Enum):
    """ゲームの状態を表す列挙型"""
    TITLE = auto()
    PREPARE = auto()
    PLAYING = auto()
    RESULT = auto()


class GameMode(Enum):
    """ゲームの難易度モードを表す列挙型"""
    EASY = auto()    # 足し算のみ
    NORMAL = auto()  # 足し算と引き算
    HARD = auto()    # 足し算、引き算、掛け算
