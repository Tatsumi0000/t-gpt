from os.path import dirname, join

from dotenv import load_dotenv
from llama_index.core import (
    GPTVectorStoreIndex,
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

from ..confluence.LoadConfluenceDocument import LoadConfluenceDocument


class CreateGeminiIndex(object):
    """文書をGeminiのLLMで使うためにベクトル化するクラス
    Attributes:
        llm_model(str): LLMの使用モデル
        embed_model(str): 文書のベクトル化(embed)に使うモデル名
        current_dirname(str): このファイルのディレクトリパス
        save_index_dir_name(str): 作成したindexを保存するディレクトリ名
    """

    def __init__(
        self,
        llm_model: str = "models/gemini-1.5-flash",
        embed_model: str = "models/embedding-001",
        save_index_dir_name: str = "./index_data",
    ):
        """コンストラクタ
        Parameters:
            llm_model(str): LLMの使用モデル
            embed_model(str): 文書のベクトル化(embed)に使うモデル名
            save_index_dir_name(str): 作成したindexを保存するディレクトリ名
        """
        self.current_dirname = dirname(__file__)
        self.llm_model = llm_model
        self.embed_model = embed_model
        self.save_index_dir_name = join(self.current_dirname, save_index_dir_name)
        self.setup_env()
        self.setup_gemini()

    def setup_env(self) -> None:
        """環境変数をセットアップする"""
        dotenv_path = join(self.current_dirname, "../../.env")
        load_dotenv(dotenv_path)

    def setup_gemini(self) -> None:
        """使用するGeminiのモデルを設定する"""
        Settings.llm = GoogleGenAI(model_name=self.llm_model)
        Settings.embed_model = GoogleGenAIEmbedding(model_name=self.embed_model)

    def create_and_save_index(self) -> None:
        """LLMに渡すために文書のindex化&保存

        indexの再生成はコストがかかるので生成後は保存する
        """
        load_confluence_document = LoadConfluenceDocument()
        documents = load_confluence_document.load_data()
        index = GPTVectorStoreIndex.from_documents(documents)
        save_dir = join(self.current_dirname, self.save_index_dir_name)
        index.storage_context.persist(save_dir)

    def ask_question(self, question: str):
        """質問をする

        indexデータは再生成するのではなくすでに保存しているものを流用する
        先に保存していないとエラーになる。検証に使う
        Parameters
            question(str): 質問内容
        """
        storage_context = StorageContext.from_defaults(
            persist_dir=self.save_index_dir_name
        )
        index = load_index_from_storage(storage_context)
        query_engine = index.as_query_engine()
        print(query_engine.query(question))


if __name__ == "__main__":
    print("start!!!")
    create_gemini_index = CreateGeminiIndex()
    create_gemini_index.create_and_save_index()
    question = "何のAndroidアプリを作っていますか?"
    create_gemini_index.ask_question(question)
