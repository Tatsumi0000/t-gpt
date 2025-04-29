from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.bridge.langchain import PromptTemplate
from llama_index.core.prompts import ChatPromptTemplate

from ..base.Base import is_development
from .GeminiBase import GeminiBase


class AskGemini(GeminiBase):
    """Geminiに質問するクラス"""

    def __init__(self) -> None:
        super().__init__(__file__)

    def query(self, dataset_name: str, question: str) -> RESPONSE_TYPE:
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
            >>> ask_gemini = AskGemini()
            >>> question = "作っているアプリは何ですか？"
            >>> answer = ask_gemini.query("android", question)
            >>> print(answer) # LLMからの回答結果
            >>> for ans in answer.source_nodes:
            >>>     print(f'{ans.metadata["title"]}: {ans.metadata["url"]}')

        """

        if is_development:
            storage_context = StorageContext.from_defaults(
                persist_dir=self.save_index_file_dir_path(dataset_name)
            )
            index = load_index_from_storage(storage_context)
            query_engine = index.as_query_engine()
            return query_engine.query(question)

    def prompt_tuning(self):
        """Geminiに問い合わせるためのプロンプトをカスタマイズ

        TODO: 後でいい感じにプロンプトをチューニングしてあげる
        """
        # a = ChatPromptTemplate()
        pass


if __name__ == "__main__":
    print("質問します！！！！！！")
    question = "誰がアプリを作っていますか?"
    ask_gemini = AskGemini()
    answer = ask_gemini.query("android", question)
    print(answer)
    for ans in answer.source_nodes:
        print("---------")
        print(f'{ans.metadata["title"]}: {ans.metadata["url"]}')
    print("終了")
