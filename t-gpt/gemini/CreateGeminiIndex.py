import os
from os.path import dirname, join

from dotenv import load_dotenv
from llama_index.core import GPTVectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI


class CreateGeminiIndex:
    def __init__(
        self, llm_model="models/gemini-1.5-flash", embed_model="models/embedding-001"
    ):
        """
        コンストラクタ
        :param llm_model: str
            LLMの使用モデル
        :param embed_model: str
            文書のベクトル化(embed)に使うモデル名
        """
        self.llm_model = llm_model
        self.embed_model = embed_model
        self.setup_env()
        self.setup_gemini()

    def setup_env(self) -> None:
        """
        環境変数をセットアップする
        """
        self.current_dirname = dirname(__file__)
        dotenv_path = join(self.current_dirname, "../../.env")
        load_dotenv(dotenv_path)

    def setup_gemini(self):
        """
        使用するGeminiのモデルを設定する
        """
        Settings.llm = GoogleGenAI(model_name=self.llm_model)
        Settings.embed_model = GoogleGenAIEmbedding(model_name=self.embed_model)

    def create_index(self):
        documents = SimpleDirectoryReader(
            join(self.current_dirname, "data")
        ).load_data()
        index = GPTVectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        print(
            query_engine.query(
                "ジャンプ流!DVD付分冊マンガ講座(8) 2016年 5/2 号では何が見れますか？"
            )
        )


if __name__ == "__main__":
    print("start!!!")
    create_gemini_index = CreateGeminiIndex()
    create_gemini_index.create_index()
