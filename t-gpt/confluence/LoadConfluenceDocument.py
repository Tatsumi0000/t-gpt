import os
from os.path import dirname, join
from typing import List

from dotenv import load_dotenv
from llama_index.core.readers import Document
from llama_index.readers.confluence import ConfluenceReader

from ..base.Base import Base


class LoadConfluenceDocument(Base):
    """Confluenceからドキュメントを読み込む
    Attributes:
        label(str): 収集したいドキュメントに付与されているlabel
        reader(ConfluenceReader): ConfluenceReaderのインスタンス
    """

    def __init__(self, label: str = "android") -> None:
        """コンストラクタ
        Parameters:
            label(str): 収集したいドキュメントに付与されているlabel
        """
        super().__init__(__file__)
        self.label = label
        self.create_reader()

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
