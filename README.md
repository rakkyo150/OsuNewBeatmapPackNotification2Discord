# OsuNewBeatmapPackNotification2Discord
osu!stdのビートマップパックの更新があったらwebhookに通知を投げるやつ。<br>
Discord以外で動くかは分からないです。<br>
最初の実行では最新のosu!stdのビートマップパックひとつだけが通知されますが、以降は更新された分だけ通知されます。<br>
**Herokuでデプロイする場合はmasterブランチではなく[herokuブランチ](https://github.com/rakkyo150/OsuNewBeatmapPackNotification2Discord/tree/heroku)をお使いください。**<br>
Herokuでデプロイできるようにrequirements.txtとruntime.txtは入れているので、各自でデプロイして使ってください。<br>

**2023年3月10日追記**<br>
なお、HerokuブランチはサイトのHTMLの変更に伴い、2023年3月10日ごろから正常に動作しなくなりました。<br>
そのため、2023年3月10日現在以降はテスト環境の構築が困難なため、メンテする予定はありません。<br>
どうしても使いたい場合は、各自でmasterブランチの変更を取り込んでください。<br>

## Quick Start
```bash
# Comfirm
$ python -V
$ apt -v
# Clone
$ sudo apt update
$ sudo apt install git
$ git clone https://github.com/rakkyo150/OsuNewBeatmapPackNotification2Discord
$ cd OsuNewBeatmapPackNotification2Discord
# Auto Setting
$ source initialization.sh
# Edit cron for scheduled execution
$ crontab -e
```


## Step by Step
### 環境確認
aptとpythonが使えることが前提となります<br>
不安な方は以下のコマンド確認できます。<br>
一応私の環境で実行した結果も表示しておきます。
```bash
$ python -V
Python 3.9.2
$ apt -v
apt 2.2.4 (arm64)
```

### リポジトリをクローン
```bash
$ sudo apt update
$ sudo apt install git
$ git clone https://github.com/rakkyo150/OsuNewBeatmapPackNotification2Discord
$ cd OsuNewBeatmapPackNotification2Discord
```
これ以降はOsuNewBeatmapPackNotification2Discordディレクトリ以下の操作になります。

### 初回実行まで
#### 自動
以下のコマンドで初期設定ができます。<br>
定期実行の設定は別で行ってください。
```bash
$ source initialization.sh
```
うまくいかない場合のために、以下に手動で設定を行う場合の手順を示しておきます。

#### 手動
1. Chromedriverインストール(chromium-browserなどは自動でダウンロードされます)
```bash
$ sudo apt install chromium-chromedriver
```

2. 仮想環境作成・ライブラリインストール
```bash
$ python venv -m venv[好きなフォルダ名]
$ venv/bin/python -m pip install -r requirements.txt
```


3. 環境変数設定
.envファイルを作成して、お好きなテキストエディタで編集してください。<br>
vimなら
```bash
$ vim .env
```
を実行した後、iを入力して編集モードに入りましょう。<br>
そして、以下を入力してください。
```bash
WEBHOOK_URL=[DiscordのwebhookのURL]
USER_NAME=[osuのアカウントのユーザーネーム]
PASSWORD=[osuのアカウントのパスワード]
```
入力が終わったら、escapeで編集終了で:wqで上書きできます。<br>

4. 初回実行(テスト)
ここまでうまく設定できていれば
```bash
$ venv/bin/python main.py
```
を実行してみると通知がくるはずです。<br>
通知が来ない場合は、ここまでうまくいっているか確認してみましょう。


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
Herokuで使用している機能が有料化されるそうなので、ラズパイなどのサーバーで使用できるようにしました(2022/9/26)<br>
ラズパイ用にREADME更新(2022/12/28)<br>
環境構築を簡単にできるようにしました(2023/2/16)<br>
サイトのHTMLの変更に対応しました(2023/3/10)
