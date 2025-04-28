from os.path import join

from .GeminiBase import GeminiBase
from llama_index.core import (
    GPTVectorStoreIndex,
    Settings,
)
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

from ..base.Base import is_development, is_production
from ..document_reader.LoadConfluenceDocument import LoadConfluenceDocument


class CreateGeminiIndex(GeminiBase):
    """文書をGeminiのLLMで使うためにベクトル化するクラス。

    Attributes:
        llm_model(str): LLMの使用モデル
        embed_model(str): 文書のベクトル化(embed)に使うモデル名
    """

    def __init__(
        self,
        llm_model: str = "models/gemini-1.5-flash",
        embed_model: str = "models/embedding-001",
    ):
        """コンストラクタ
        Args:
            llm_model(str): LLMの使用モデル
            embed_model(str): 文書のベクトル化(embed)に使うモデル名
        """
        super().__init__(__file__)
        self.llm_model = llm_model
        self.embed_model = embed_model
        self.setup_gemini()

    def setup_gemini(self) -> None:
        """使用するGeminiのモデルを設定する"""
        Settings.llm = GoogleGenAI(model_name=self.llm_model)
        Settings.embed_model = GoogleGenAIEmbedding(model_name=self.embed_model)

    def create_and_save_index(self) -> None:
        """LLMに渡すために文書のindex化&保存。

        indexの再生成はコストがかかるので生成後は保存する。
        """
        for dataset_name in self.dataset_yaml:
            # 各データソースから読み込んだドキュメントを保存する一時変数
            documents = []
            for datasource_name, datasource_value in self.datasource_yaml[
                dataset_name
            ].items():
                # コンフルエンスのデータソースが存在したら取り込む
                if datasource_name == "confluence":
                    for label in datasource_value:
                        load_confluence_document = LoadConfluenceDocument(label)
                        # 一括でindex化したいので一時変数に追加
                        documents.extend(load_confluence_document.load_data())
                # if datasource_name == "hogehoge" ここで他のデータソースが増えたら分岐を追加する
            # データセットに対するデータソースを全部探索したらindex化
            index = GPTVectorStoreIndex.from_documents(documents)
            if is_development:
                save_dir = self.save_index_file_dir_path(dataset_name)
                index.storage_context.persist(save_dir)
            elif is_production:
                pass


if __name__ == "__main__":
    print("start!!!")
    create_gemini_index = CreateGeminiIndex()
    create_gemini_index.create_and_save_index()
