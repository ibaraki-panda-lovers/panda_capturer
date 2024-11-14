# パンダキャプチャー🐼

[Hack the Disinfo 2024](https://www.disinfo2024.code4japan.org/Hack-the-Disinfo-2024-7a203c2034a240bf88ff3017d8802fcd)
の(受賞)作品です。

複数名からなるチーム「茨城パンダ愛好会」が開発したものです。

## 作品概要
「パンダキャプチャー🐼」は、中国で主要なメディアであるショート動画を証拠保全し、また内容に関するレポートをGoogle Driveに自動生成してくれるWebアプリです。

中国には様々なショート動画アプリが存在し、主要なメディアとなっています。
偽情報もショート動画として出回ることが多く、中国語ショート動画の分析は重要なタスクです。

しかし、中国語ショート動画の分析には以下のような課題があります。

1. 文責対象の偽動画が検閲で消されてしまう（証拠保全の問題）
2. 内容が中国語で分からない・聞き取れない
3. スマホで見つけた動画を後からPCで分析したい

「パンダキャプチャー🐼」は、
最低限の動画情報と動画本体をアップロードするだけで、
動画本体と以下の内容が含まれた分析レポートを自動でGoogle Driveに保存します。

 - 動画情報
 - 動画内容の中国語文字起こし ([AmiVoice API](https://acp.amivoice.com/amivoice_api/)を利用)
 - 中国語文字起こしの翻訳結果 ([DeepL API](https://www.deepl.com/ja/pro-api)を利用)
 - 中国語ファクトチェックサイトの関連する記事を提示 ([chinafactcheck.com](https://chinafactcheck.com/)のスクレイピングデータを利用)

 これにより、上記の課題を解決できます。

## 環境構築
「パンダキャプチャー🐼」を動作させるための環境構築方法は以下の通りです。

Dockerを利用していますが、API等の事前設定が必要になります。

### `.env`の作成
`.env-templete`ファイルを`.env`としてコピーします。
### ドメインの取得
Google認証(Login with Google)の仕様により、動作にはドメインが必要になります。

サービスを動作させるURIを`.env`の`REDIRECT_URI`に記述します。
末尾の`/`はつけないでください。
(e.g. `https://example.com`)

### AmiVoice API
AmiVoiceのAPIキーを`.env`の`AMIVOICE_ONETIME_TOKEN`に設定してください。

セキュリティ上の理由から、[ワンタイム APPKEY](https://docs.amivoice.com/amivoice-api/manual/one-time-app-key/)の使用を強く推奨します。

### DeepL API
DeepL APIのAPIキーを`.env`の`DEEPL_API_KEY`に設定してください。

### Google API
Google認証(Login with Google)とGoogle Driveへの書き込みが行えるようにGoogle APIを設定し、
`client_secret.json`を`app/client_secret.json`に保存してください。

 - 認証と認可の詳細 | Google Workspace | Google for Developers - https://developers.google.com/workspace/guides/auth-overview?hl=ja
 - Google Drive API のスコープを選択する | Google for Developers - https://developers.google.com/drive/api/guides/api-specific-auth?hl=ja

### Cloudflare Tunnelの設定
[Cloudflare Tunnel](https://www.cloudflare.com/ja-jp/products/tunnel/)を設定します。

先に設定した`REDIRECT_URI`とコンテナ内の
アプリケーション`http://localhost:8008/`をトンネルします。

`TUNNEL_TOKEN`を`.env`に設定します。

`REDIRECT_URI`はデフォルトでは全世界に公開されるため、必要に応じてアクセス制限をしてください。

## 実行方法

```sh
$ docker compose up -d --build
```

`REDIRECT_URI`でサービスが公開されます。

## 制約事項
- Cloudflare Tunnelの制限で100MBまでしかアップロードできません
- 以下のファイルを自動更新する機能はありません
  - `chinafactcheck.com`のスクレイピングデータ: `app\factcheck_articles_with_url_content_C.json`
  - 上記データをTF-IDFでベクトル化したもの: `app\tfidf_embeddings.pkl`
- Driveへの書き込みはルートフォルダに行われます、フォルダの選択ではできません。
- 突貫工事の成果物なので、可読性とかセキュリティとかは不完全だと思います。

## 謝辞
チームメンバー、ハッカソン運営・審査員の皆様、他チームの皆様、そしてすべての関係者の皆様にこの場を借りて御礼申し上げます。
