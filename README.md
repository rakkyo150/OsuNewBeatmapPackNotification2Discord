# OsuNewBeatmapPackNotification2Discord
osu!stdのビートマップパックの更新があったらwebhookに通知を投げるやつ。<br>
Discord以外で動くかは分からないです。<br>
最初の実行では１ページ目のすべてのosuSTDのビートマップパックが通知されますが、以降は更新分だけ通知されます。<br>
Herokuでデプロイできるようにrequirements.txtとruntime.txtは入れているので、各自でデプロイして使ってください。

デプロイに際して、postgreSQLを使えるようにしてください。<br>
Herokuだと、Heroku Postgresのアドオンを追加すればオッケーです。<br>
また、環境変数としては、DATABASE_URLにはpostgreSQLのURLを設定し、WEBHOOK_URLにディスコートのwebhookのURLを設定してください。<br>
Herokuなら、DATABASE_URLはHeroku Postgresを追加した時点で自動で設定されています。<br>
あとは、各自好きな間隔でpython main.pyで定期実行するように設定をしてください。<br>
Herokuだと、Heroku Schedulerのアドオンを追加して設定すればオッケーです。

もしデプロイとかよくわからないけど使いたい人がいれば、その旨を伝えてもらえればwebhookのURLを登録するだけで使えるようにしようと思っています。

## Change Log
バグ修正(2021/7/29)
さらにバグ修正(2021/8/2)
