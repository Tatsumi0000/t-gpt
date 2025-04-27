## t-gpt

llamaindexを使って外部ファイルをindexとして保存しその情報を元にLLM(Gemini)に質問&回答をもらうシステムです。
現時点ではConfluenceにのみ対応しています。
GPTVectorStoreIndexを使ってファイルベースでindex化を行います。

## 開発

Slackの開発設定で
- `OAuth & Permissions`で`chat.write`権限を付与してください。これがないとSlackに投稿できません。
- `Subscribe to bot events`で`app_mention`権限を付与してください。これがないとメンションをもらっても反応できません。

```
brew install ngrok
docker run -it --rm -p 8080:8080 -v $(PWD):/app t-gpt  /bin/bash -c "poetry run python -m t-gpt.slack.Slack"
ngrok http http://localhost:8080
```
