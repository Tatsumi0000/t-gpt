from os.path import join

from llama_index.core import (
    GPTVectorStoreIndex,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

from ..base.Base import Base, is_development, is_production
from ..document_reader.LoadConfluenceDocument import LoadConfluenceDocument


class CreateGeminiIndex(Base):
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
                save_dir = join(
                    self.current_dirname, self.save_index_file_dir_path(dataset_name)
                )
                index.storage_context.persist(save_dir)
            elif is_production:
                pass

    def ask_question(self, dataset_name: str, question: str) -> RESPONSE_TYPE:
        """質問をする

        indexデータは再生成するのではなくすでに保存しているものを流用する。
        先に保存していないとエラーになる。検証に使う。

        Args:
            dataset_name(str): 質問したいデータセット名
            question(str): 質問内容

        Returns:
            質問した内容に対する回答。
            返り値の中のsource_nodes.metadataから参考にしたドキュメントのタイトル(title)とURL(url)を取得できる。
            単純に返り値を出力した場合は回答内容が取れる。

        Examples:
            >>> create_gemini_index = CreateGeminiIndex()
            >>> question = "作っているアプリは何ですか？"
            >>> answer = create_gemini_index.ask_question("android", question)
            >>> print(answer) # LLMからの回答結果
            >>> for ans in answer.source_nodes:
            >>>     print(f'{ans.metadata["title"]}: {ans.metadata["url"]}')

        """
        storage_context = StorageContext.from_defaults(
            persist_dir=self.save_index_file_dir_path(dataset_name)
        )
        index = load_index_from_storage(storage_context)
        query_engine = index.as_query_engine()
        return query_engine.query(question)

    def save_index_file_dir_path(self, dataset_name: str) -> str:
        """index化したデータを保存するディレクトリパスを生成。

        ${dataset_name}_index_data というディレクトリ名で保存する。

        Args:
            dataset_name(str): データセット名

        Returns:
            パス形式で返す
        """
        dir_name = self.save_index_file_dir_name(dataset_name)
        return f"{join(self.current_dirname, dir_name)}"

    def save_index_file_dir_name(self, dataset_name: str) -> str:
        """index化したデータを保存するディレクトリ名を生成。

        ${dataset_name}_index_data というディレクトリ名にする。

        Args:
            dataset_name(str): データセット名

        Returns:
            ${dataset_name}_index_data という形式で返す
        """
        return f"{dataset_name}_index_data"


if __name__ == "__main__":
    print("start!!!")
    create_gemini_index = CreateGeminiIndex()
    create_gemini_index.create_and_save_index()
    # question = "誰がアプリを作っていますか?"
    #
    # answer = create_gemini_index.ask_question("android", question)
    # print(answer)
    # for ans in answer.source_nodes:
    #     print("---------")
    #     print(f'{ans.metadata["title"]}: {ans.metadata["url"]}')
