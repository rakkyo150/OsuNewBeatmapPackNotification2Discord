# OsuNewBeatmapPackNotification2Discord
osu!stdのビートマップパックの更新があったらwebhookに通知を投げるやつ。<br>
Discord以外で動くかは分からないです。<br>
最初の実行では最新のosu!stdのビートマップパックひとつだけが通知されますが、以降は更新された分だけ通知されます。<br>
**Herokuでデプロイする場合はmasterブランチではなく[herokuブランチ](https://github.com/rakkyo150/OsuNewBeatmapPackNotification2Discord/tree/heroku)をお使いください。**<br>
Herokuでデプロイできるようにrequirements.txtとruntime.txtは入れているので、各自でデプロイして使ってください。

## 設定方法
数か月前にやったことを思い出して書いているので、なにか抜けてる部分があるかもです。<br>
もしエラー等があったら適宜うまく対応してもらえるとありがたいです。

### 適当なディレクトリで以下を実行
```bash
$ sudo apt update
$ sudo apt install git
$ git clone https://github.com/rakkyo150/OsuNewBeatmapPackNotification2Discord
$ cd OsuNewBeatmapPackNotification2Discord
```

### Postgresql環境構築
https://raspi.taneyats.com/entry/install-postgresql<br>
上記URLの「ユーザー(ロール)にパスワードを設定」まで設定をしましょう。<br>
その後、
```bash
$ su - postgres
パスワード:
$ createdb [好きなデータベース名]
$ exit
```
でデータベースを作成しておきましょう。<br>
参考 : https://www.postgresql.org/docs/11/reference-client.html

### Chromiumインストール
```bash
$ sudo apt install chromium-chromedriver
```

### 仮想環境構築・仮想環境に入る
```bash
$ python venv -m hogehoge[好きなフォルダ名]
$ source hogehoge\Scripts\activate
```

### ライブラリインストール
```bash
(hogehoge) $ pip install -r requirements.txt
```

### 環境変数設定
.envファイルを作成して、お好きなテキストエディタで編集してください。<br>
vimなら
```bash
(hogehoge) $ vim .env
```
を実行した後、iを入力して編集モードに入りましょう。<br>
そして、以下を入力してください。
```bash
DATABASE_URL=postgresql://[サーバーのIPアドレス]:[postgresのポート番号でデフォルトは5432]/[作成したデータベース名]?user=[作成したユーザ名]&password=[設定したパスワード]
WEBHOOK_URL=[DiscordのwebhookのURL]
USER_NAME=[osuのアカウントのユーザーネーム]
PASSWORD=[osuのアカウントのパスワード]
```
入力が終わったら、escapeで編集終了で:wqで上書きできます。<br>

### テスト
ここまでうまく設定できていれば
```bash
(hogehoge) $ hogehoge/bin/python main.py
```
を実行してみると通知がくるはずです。<br>
通知が来ない場合は、ここまでうまくいっているか確認してみましょう。<br>
もう一度テストする場合は、データベースにデータが追加されている場合はそのデータは削除してからテストしてみてください。<br>
うまくいったら仮想環境から出ても大丈夫です。
```bash
(hogehoge) $ deactivate
```

### 定期実行の設定
ラズパイなら
```sh
$ crontab -e
```
から、毎時0分ごとに実行なら、最下部に
```cron
0 * * * * cd OsuNewBeatmapPackNotification2Discord; hogehoge/bin/python main.py
```
を追加して上書き保存してください。<br>
詳しくはcronの書き方を検索して調べてみてください。

## Change Log
バグ修正(2021/7/29)<br>
さらにバグ修正(2021/8/2)<br>
URL (https://osu.ppy.sh/beatmaps/packs) も通知内容に含めました(2021/8/16)<br>
初回実行時のバグを修正 & ビートマップパックごとのダウンロードURLを通知に追加 & 通知に埋め込みを使用(2021/8/16)<br>
安定化(2021/8/19)<br>
ダウンロードリンクがなぜか取れないことがあったのでその対策(2021/8/21)<br>
Herokuで使用している機能が有料化されるそうなので、ラズパイなどのサーバーで使用できるようにしました(2022/9/26)
ラズパイ用にREADME更新(2022/12/28)
