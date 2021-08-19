# OsuNewBeatmapPackNotification2Discord
osu!stdのビートマップパックの更新があったらwebhookに通知を投げるやつ。<br>
Discord以外で動くかは分からないです。<br>
最初の実行では１ページ目のすべてのosuSTDのビートマップパックが通知されますが、以降は更新分だけ通知されます。<br>
Herokuでデプロイできるようにrequirements.txtとruntime.txtは入れているので、各自でデプロイして使ってください。

## デプロイ方法

Heroku Postgresのアドオンを追加すればオッケーです。<br>
Heroku Schedulerのアドオンを追加して、好きな間隔でpython main.pyを定期実行する設定をしてください。<br>
seleniumを使用しているので、ビルドパックに https://github.com/heroku/heroku-buildpack-google-chrome と https://github.com/heroku/heroku-buildpack-chromedriver を追加してください。

また、環境変数としては、<br>
- DATABASE_URL:postgreSQLのURL（自動で追加されています）
- WEBHOOK_URL:DiscordのwebhookのURL
- CHROME_DRIVER:/app/.chromedriver/bin/chromedriver
- USER_NAME:osuのアカウントのユーザーネーム
- PASSWORD:osuのアカウントのパスワード
を設定してください。<br>


## Change Log
バグ修正(2021/7/29)<br>
さらにバグ修正(2021/8/2)<br>
URL (https://osu.ppy.sh/beatmaps/packs) も通知内容に含めました(2021/8/16)<br>
初回実行時のバグを修正 & ビートマップパックごとのダウンロードURLを通知に追加 & 通知に埋め込みを使用(2021/8/16)
