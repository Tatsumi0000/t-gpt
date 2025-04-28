import os

from slack_bolt import App

from ..gemini.CreateGeminiIndex import CreateGeminiIndex
from ..slack.SlackAppMention import SlackAppMention

"""Slackから返ってきたイベントに対して色々反応する関数たち
"""

slack_app_mention = SlackAppMention(__file__)
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.event("app_mention")
def handle_message_events(event, say):
    """メンションされたらこの関数が呼ばれる

    ユーザが指示したデータセットと質問内容を判断し、
    適切なindexを使ってGeminiに問い合わせた後、Slackの質問してきたスレに返答
    """
    slack_app_mention.initialize(event)
    # 改行コードで分割する。最初にほしいデータセットが入っていることを期待
    lines = slack_app_mention.text_without_mentions.splitlines()

    # サイズが1だと@t-gpt hoge みたいな形式でメッセージが返っている
    # この場合は質問ではないのでそのコマンドに応じた返答をする
    if len(lines) == 1:
        command = lines[0].strip().lower()
        if command == "ping":
            say(
                text=slack_app_mention.ping_message(),
                thread_ts=slack_app_mention.thread_ts,
            )
            return
        elif command == "help":
            help_message = slack_app_mention.help_message()
            say(
                text=help_message[0],
                blocks=[
                    help_message[1],
                    help_message[2],
                    slack_app_mention.footer_message(),
                ],
                thread_ts=slack_app_mention.thread_ts,
            )
            return
        else:
            say(
                text="そのコマンドには対応していません。",
                thread_ts=slack_app_mention.thread_ts,
            )
            return
    elif len(lines) >= 2:
        say(
            text="回答を生成中です。しばらくお待ちください。",
            thread_ts=slack_app_mention.thread_ts,
        )
        dataset_name = lines[0].strip()
        # データセットが対応してない場合
        if not slack_app_mention.contains_dataset_name(dataset_name):
            message = f"データセット「{dataset_name}」は対応していません。"
            say(
                text=message,
                blocks=[
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": message},
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "もしよければデータの作成にご協力ください！",
                        },
                    },
                    slack_app_mention.footer_message()[0],
                    slack_app_mention.footer_message()[1],
                ],
                thread_ts=slack_app_mention.thread_ts,
            )
            return
        create_gemini_index = CreateGeminiIndex()
        # 質問を改行してくるかもしれないので結合してあげる。
        question = "".join(lines[1:])
        answer = create_gemini_index.ask_question(dataset_name, question)
        say(
            text=str(answer),
            blocks=[
                slack_app_mention.answer_message(answer),
                slack_app_mention.reference_anchors(answer.source_nodes),
                slack_app_mention.footer_message()[0],
                slack_app_mention.footer_message()[1],
            ],
            thread_ts=slack_app_mention.thread_ts,
        )
    if not slack_app_mention.text_without_mentions:
        print("メンションのみで空文字です。")
    else:
        print("メッセージが詰まってます。")


if __name__ == "__main__":
    app.start(port=int(8080))
