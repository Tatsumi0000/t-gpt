## t-gpt

llamaindexを使って外部ファイルをindexとして保存しその情報を元にLLM(Gemini)にSlack上で質問&回答をするSlack Appです。
現時点ではConfluenceにのみ対応しています。
GPTVectorStoreIndexを使ってファイルベースでindex化を行います。

SlackのHTTPモードで動作します。
Socketモードでの動作させたい場合は、`./t-gpt/slack/event_handler.py`を編集してください。

## 開発

Slackの開発設定で
- `OAuth & Permissions`で`chat.write`権限を付与してください。これがないとSlackに投稿できません。
- `Subscribe to bot events`で`app_mention`権限を付与してください。これがないとメンションをもらっても反応できません。

SlackのHTTPモードではパブリックなエンドポイントを準備する必要があるのでngrokを使用します(いずれcomposeを使っていい感じにする)。

```sh
brew install ngrok
docker run -it --rm -p 8080:8080 -v $(PWD):/app t-gpt  /bin/bash -c "poetry run python -m t-gpt.slack.event_handler"
ngrok http http://localhost:8080
```

### env
環境変数をセットする。
```sh
ENV='development|production|test'
OPENAI_API_KEY='OpenAIのキー（今はOpenAIには対応してない）'
GOOGLE_API_KEY='Geminiを使うためのキー'
CONFLUENCE_BASE_URL='コンフルエンスのURL（~~~/wikiまでを記入）'
CONFLUENCE_USERNAME='コンフルエンスのユーザ名（データを取得するために必要）'
CONFLUENCE_PASSWORD='コンフルエンスのAPI_KEY（Atlassianの管理画面から取る）'
SLACK_BOT_TOKEN='xoxb-で始まるSlackキー'
SLACK_SIGNING_SECRET='Slackの管理画面にあるSiging Secretの値'
```

## yaml
`config`のymlファイルで設定をします。

### dataset.yml
データセットを定義します。

データセット・・・indexファイルを分割する単位

ドキュメントをindex化する時に対象ドキュメントが多くなるとindexファイルが巨大化し、アプリのパフォーマンスが悪化する可能性があります。そのため事前に特定の分類ごとにindexファイルを分割して管理できるようにしています。

### datasource.yml
index化したいドキュメントをどこから取得するか定義します。

データソース・・・データセットに対してどこからドキュメントを取得するか

現時点ではConfluenceのみに対応しています。Confluenceのデータは付与されているラベルでドキュメントを取ります。

```yml
android: # データセット名（dataset.ymlに定義してあるものを指定）
  confluence: # 取得するデータの管理対象
    - android # 取得したいドキュメントに付与されているラベル
    - fuga
  google_slides: # いずれ対応したいGoogle Slides
    - URL1 # 取得したいURLをベタ書き
    - URL2
ios: # データセット名
  confluence:
    - ios
    - swift
```

