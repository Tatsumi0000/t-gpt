import os
from os.path import dirname, join

from dotenv import load_dotenv


class Base(object):
    """各クラスで継承するための元クラス

    RailsみたいにRails.env.production的なことをしたいので親クラスで読み込んで使い回す
    それ以外は基本的に実装しない

    Attributes:
    ----------
        current_dir(str): 各コードのディレクトリ
    """

    def __init__(self, file_name: str) -> None:
        """コンストラクタ。環境変数を読み込む

        Parameters:
        -----------
        file_name(str): ファイル名
        """
        self.current_dirname = dirname(file_name)
        self.setup_env()

    def setup_env(self) -> None:
        """環境変数をセットアップする"""
        dotenv_path = join(self.current_dirname, "../../.env")
        load_dotenv(dotenv_path)


def is_development() -> bool:
    """開発モードかどうか。ローカルでの開発中で使う想定"""
    return os.environ["ENV"] == "development"


def is_production() -> bool:
    """本番かどうか。本番実行中でのみ使う想定"""
    return os.environ["ENV"] == "production"


def is_test() -> bool:
    """testかどうか。testで使う想定"""
    return os.environ["ENV"] == "test"
