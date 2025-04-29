## t-gpt

llamaindexを使って外部ファイルをindexとして保存しその情報を元にLLM(Gemini)にSlack上で質問&回答をするSlack Appです。
現時点ではConfluenceにのみ対応しています。
GPTVectorStoreIndexを使ってファイルベースでindex化を行います。

SlackのHTTPモードで動作します。
Socketモードでの動作させたい場合は、`./t-gpt/slack/event_handler.py`を編集してください。

## 開発
docker composeを使って開発しています。

### indexファイルの生成

indexファイルを事前に作るために以下のコマンドを実行してください。
事前に学習用のデータをConfluenceなどに準備して実行してください。

```sh
make dev/setup
make dev/run
poetry run python -m t-gpt.gemini.CreateGeminiIndex
docker compose up
```

docker-composeを立ち上げたら`loalhost:4040`にブラウザでアクセスし、`表示されたURL/slack/events`をSlackの管理画面にある`Event Subscriptions`の`Request URL`にURLを指定します。
正しく起動できていれば`Verified`になります。

ngrokのコンテナを立ち上げるたびにproxyするURLが変わるので基本的にはngrokのコンテナは立ち上げっぱなしがおすすめです。

### Slackの設定
Slackのトークンを取得してenvにセットする必要があります。
Slackの開発設定で
- `OAuth & Permissions`で`chat.write`権限を付与してください。これがないとSlackに投稿できません。
- `Subscribe to bot events`で`app_mention`権限を付与してください。これがないとメンションをもらっても反応できません。


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
SLACK_SIGNING_SECRET='Slackの管理画面にあるSigning Secretの値'
NGROK_AUTHTOKEN='ngrokのトークン'
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

