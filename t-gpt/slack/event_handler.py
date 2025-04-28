import os
import re

from slack_bolt import App

from ..base.Base import Base
from ..slack.SlackAppMention import SlackAppMention

"""Slackから返ってきたイベントに対して色々反応する関数たち
"""
base = Base(__file__)
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.event("app_mention")
def handle_message_events(event, say):
    """メンションされたらこの関数が呼ばれる

    ユーザが指示したデータセットと質問内容を判断し、
    適切なindexを使ってGeminiに問い合わせ後Slackの質問してきたスレに返答
    """
    slack_app_mention = SlackAppMention(event)
    # 改行コードで分割する。最初にほしいデータセットが入っていることを期待
    lines = slack_app_mention.text_without_mentions.splitlines()

    # サイズが1だと@t-gpt hoge みたいな形式でメッセージが返っている
    # この場合は質問ではないのでそのコマンドに応じた返答をする
    if len(lines) == 1:
        if lines[0] in "ping":
            say(
                text=slack_app_mention.ping_message(),
                thread_ts=slack_app_mention.thread_ts,
            )
            return
        elif lines[0] in "help":
            help_message = slack_app_mention.help_message()
            say(
                text=help_message[0],
                blocks=[help_message[1], help_message[2]],
                thread_ts=slack_app_mention.thread_ts,
            )
            return
    say(
        text="回答を生成中です。しばらくお待ちください。",
        thread_ts=slack_app_mention.thread_ts,
    )
    if not slack_app_mention.text_without_mentions:
        print("メンションのみで空文字です。")
    else:
        print("メッセージが詰まってます。")


if __name__ == "__main__":
    app.start(port=int(8080))
