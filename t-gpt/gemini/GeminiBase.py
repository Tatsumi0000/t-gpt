from os.path import join

from llama_index.core import Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

from ..base.Base import Base


class GeminiBase(Base):
    """Geminiに問い合わせする時に使う便利クラス

    Parameters:
        file(str): ファイル名
        llm_model(str): 使用するLLMのモデル名
        embed_model(str): index化する時に使うモデル名
    """

    def __init__(
        self,
        file: str,
        llm_model: str = "models/gemini-2.5-flash",
        embed_model: str = "text-embedding-004",
    ) -> None:
        """コンストラクタ

        Args:
            file(str): ファイル名
        """
        super().__init__(file)
        self.llm_model = llm_model
        self.embed_model = embed_model

    def setup_gemini(self) -> None:
        """使用するGeminiのモデルを設定する"""
        Settings.llm = GoogleGenAI(model_name=self.llm_model)
        Settings.embed_model = GoogleGenAIEmbedding(model_name=self.embed_model)

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
