import re
from typing import List

from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.schema import NodeWithScore

from ..base.Base import Base


class SlackAppMention(Base):
    """Slackで返信する時に使うクラス
    各メソッドやメンバ変数を使う前にコンストラクタ->イニシャライザで初期化して使うことを想定している

    Params:
        user(str): メンションしてきたユーザ
        text(str): ユーザが送ってきたメッセージ
        thread_ts(str): スレ中でのメンションならその中に、新規だったらそのメンションの中にスレを作る
    """

    def __init__(self, file) -> None:
        """コンストラクタ

        Args:
            file(str): 実行するファイルのパス
        """
        super().__init__(file)

    def initialize(self, event) -> None:
        """イニシャライザ
        コンストラクタはslack_boltを使うために一度環境変数を読み込ませる
        イニシャライザでは、Slackからメンションされた時に呼び出される変数をセットする

        Args:
            event: Slackから返ってきたEvent。中に色々情報が詰まってる
        """
        self.event = event
        self.user = event.get("user")
        self.text = event.get("text")
        self.thread_ts = event.get("thread_ts") or event.get("ts")
        self.text_without_mentions = self._text_without_mentions()

    def _text_without_mentions(self) -> str:
        """ユーザが送ってきたメッセージからメンション部分を削ぎ落として返す"""
        return re.sub(r"<@([A-Z0-9]+)>", "", self.text)

    def answer_message(self, answer: RESPONSE_TYPE) -> dict:
        """LLMから返ってきた回答をblock形式で返す

        Args:
            answer(RESPONSE_TYPE): LLMから返ってきた回答

        Returns:
            Slackのblock形式に合わせた回答
        """
        return {"type": "section", "text": {"type": "mrkdwn", "text": str(answer)}}

    def reference_anchors(self, refs: List[NodeWithScore]) -> dict:
        """LLMから返ってきたレスポンスがどのドキュメントを参考にしたかをSlack形式のアンカーのListで返す

        Args:
            refs(List[NodeWithScore]): LLMから返ってきた参考にしたmetadata一覧

        Returns:
            Slack形式のアンカーを箇条書きのblockで返す
            Slack形式のアンカー = <url|title>
        """
        anchors = []
        for ref in refs:
            title = ref.metadata["title"]
            url = ref.metadata["url"]
            anchors.append(f"• <{url}|{title}>")
        anchor_text = "\n".join(anchors)
        return {"type": "section", "text": {"type": "mrkdwn", "text": anchor_text}}

    def help_message(self) -> tuple[str, dict, dict]:
        """helpコマンドが返ってきた時にメッセージを返す

        Returns:
            タプル形式で返す。
            messageはそのままblock kitのtextにセットすることを想定
            それ以降のdictはblock kitにいれる想定

        Examples:
            >>> say(
            >>>     text=help_message()[0],
            >>>         blocks=[
            >>>             help_message()[1],
            >>>             help_message()[2]
            >>>         ]
            >>> )
        """

        message0 = f"対応しているデータセットは{",".join(self.dataset_yaml)}になります。質問は以下の形式で質問してください。\n"
        message1 = "@g-gpt データセット名\n質問内容"
        return (
            message0 + message1,
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": message0},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message1,
                },
            },
        )

    def contains_dataset_name(self, dataset_name: str) -> bool:
        """Slackから指定されたデータセット名が対応しているかどうかを返す

        Args:
            dataset_name(str): Slackから受け取ったデータセット名

        Returns:
            dataset.ymlにSlackから指定されたデータセット名が定義されているか。対応していたらTrue
        """
        return dataset_name in self.dataset_yaml

    def ping_message(self) -> str:
        """pingコマンド時に返すメッセージ

        Returns:
            メンション付きで返す
        """
        return f"<@{self.user}> ping pong!🏓"

    def footer_message(self) -> List[dict]:
        """メッセージの最後にいれるフッターを返す

        Returns:
            タプル形式で返す。最初に区切り線で、最後にメッセージ
        """
        url = "https://github.com/Tatsumi0000/t-gpt/"
        return [
            {"type": "divider"},
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"powered by <{url}|t-gpt>",
                    }
                ],
            },
        ]


if __name__ == "__main__":
    print("start")
