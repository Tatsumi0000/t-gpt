import os
from os.path import dirname, join
from typing import List

from dotenv import load_dotenv
from llama_index.core.readers import Document
from llama_index.readers.confluence import ConfluenceReader


class LoadConfluenceDocument(object):
    """Confluenceからドキュメントを読み込む
    Attributes:
        label(str): 収集したいドキュメントに付与されているlabel
        current_dirname(str): 実行しているドキュメントのパス
        reader(ConfluenceReader): ConfluenceReaderのインスタンス
    """

    def __init__(self, label: str = "android") -> None:
        """コンストラクタ
        Parameters:
            label(str): 収集したいドキュメントに付与されているlabel
        """
        self.label = label
        self.current_dirname = dirname(__file__)
        self.setup_env()
        self.create_reader()

    def setup_env(self) -> None:
        """環境変数をセットアップする

        環境変数で[CONFLUENCE_API_TOKEN]をセットしているのでライブラリが自動で認証設定を済ませる
        """
        dotenv_path = join(self.current_dirname, "../../.env")
        load_dotenv(dotenv_path)

    def create_reader(self) -> None:
        """ConfluenceReaderのインスタンスを生成"""
        self.reader = ConfluenceReader(
            base_url=os.environ["CONFLUENCE_BASE_URL"],
        )

    def load_data(self) -> List[Document]:
        """Confluenceから読み込んだドキュメント

        Returns
            List[Document]: 条件にマッチしたConfluenceのドキュメントをListで返す
        """
        cql = f'type="page" AND label="{self.label}"'
        return self.reader.load_data(cql=cql)


if __name__ == "__main__":
    load = LoadConfluenceDocument()
    docs = load.load_data()
    print(docs)
