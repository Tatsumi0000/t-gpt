import os
import re

from slack_bolt import App

from ..base.Base import Base

base = Base(__file__)

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.event("app_mention")
def handle_message_events(event, say):
    user = event.get("user")
    text = event.get("text")
    # スレ中でのメンションならその中に、新規だったらそのメンションの中にスレを作る
    thread_ts = event.get("thread_ts") or event.get("ts")
    # メンションを取り除いたメッセージ部分のみを取り出す。メンション後にスペースが入っているのでそれも削ぎ落とす
    text_without_mentions = re.sub(r"<@([A-Z0-9]+)> ", "", text)
    # 改行コードで分割する。最初にほしいデータセットが入っていることを期待
    lines = text_without_mentions.splitlines()

    # サイズが1だと@t-gpt hoge みたいな形式でメッセージが返っている
    # この場合は質問ではないのでそのコマンドに応じた返答をする
    if len(lines) == 1:
        if lines[0] == "ping":
            say(text=f"<@{user}> ping pong!🏓", thread_ts=thread_ts)
            return
        elif lines[0] == "help":
            say(
                text=f"対応しているデータセットは{base.dataset_yaml}になります。質問は以下の形式で質問してください。\n@g-gpt データセット名\n質問内容",
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"対応しているデータセットは{base.dataset_yaml}になります。質問は以下の形式で質問してください。",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "@g-gpt データセット名\n質問内容",
                        },
                    },
                ],
                thread_ts=thread_ts,
            )
            return
    say(text="回答を生成中です。しばらくお待ちください。", thread_ts=thread_ts)
    if not text_without_mentions:
        print("メンションのみで空文字です。")
    else:
        print("メッセージが詰まってます。")


if __name__ == "__main__":
    app.start(port=int(8080))
