import os
from os.path import dirname, join

import yaml
from dotenv import load_dotenv


class Base(object):
    """各クラスで継承するための元クラス

    RailsみたいにRails.env.production的なことをしたいので親クラスで読み込んで使い回す
    それ以外は基本的に実装しない

    Attributes:
        current_dir(str): 各コードのディレクトリ
        dataset_yaml(list[str]): データセットの区分設定
        datasource_yaml(dict): どこのデータソースから取得するかの設定
    """

    def __init__(self, file_name: str) -> None:
        """コンストラクタ。環境変数を読み込む

        Args:
            file_name(str): ファイル名
        """
        self.current_dirname = dirname(file_name)
        self.setup_env()
        self.setup_yaml()

    def setup_env(self) -> None:
        """環境変数をセットアップする"""
        dotenv_path = join(self.current_dirname, "../../.env")
        load_dotenv(dotenv_path)

    def setup_yaml(self) -> None:
        """データセットの設定ファイルを読み込む"""
        datasource_yaml_path = join(self.current_dirname, "../../config/datasource.yml")
        with open(datasource_yaml_path, "r") as file:
            self.datasource_yaml = yaml.safe_load(file)

        dataset_yaml_path = join(self.current_dirname, "../../config/dataset.yml")
        with open(dataset_yaml_path, "r") as file:
            self.dataset_yaml = yaml.safe_load(file)


def is_development() -> bool:
    """開発モードかどうか。ローカルでの開発中に使う想定"""
    return os.environ["ENV"] == "development"


def is_production() -> bool:
    """本番かどうか。本番実行中でのみ使う想定"""
    return os.environ["ENV"] == "production"


def is_test() -> bool:
    """testかどうか。testで使う想定"""
    return os.environ["ENV"] == "test"
