from os.path import join

from ..base.Base import Base


class GeminiBase(Base):
    """Geminiに問い合わせする時に使う便利クラス"""

    def __init__(self, file: str) -> None:
        """

        Args:
            file(str): ファイル名

        """
        super().__init__(file)

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
