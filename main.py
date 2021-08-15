import requests
from bs4 import BeautifulSoup
import json
import os

import db_handler

link="https://osu.ppy.sh/beatmaps/packs"
response=requests.get(link)
soup=BeautifulSoup(response.text,"html.parser")
packList=soup.find("div",class_="js-accordion")
topPackDiv=packList.div

topDataPackId=topPackDiv.get("data-pack-id")
topPackName=topPackDiv.a.div.text

avoidWord=["taiko","catch","mania"]

oldDataPackId=db_handler.exportOldBeatmapPack()

# 更新してるかどうか
if oldDataPackId==topDataPackId:
    pass
else:
    newPacksName=""
    newPack=False
    packDivs=packList.find_all("div",class_="beatmap-pack")
    for pack in packDivs:
        # 直近の更新までループが終わったとき
        if str(pack.get("data-pack-id"))==oldDataPackId:
            # 更新あったとき
            if newPack is True:
                db_handler.upsertNewBeatmapPack(oldDataPackId,topDataPackId)
            break
        else:
            newPack=True
            # 更新内容をosu!stdとそれ以外で分けてnewPacksNameを作る
            packName=pack.a.div.text
            if any(words in packName.lower() for words in avoidWord):
                pass
            else:
                newPacksName+=pack.a.div.text+"\n"

    # 更新内容がosu!std以外しかないorそもそも更新していない場合はディスコートに通知しない
    if newPacksName=="":
        pass
    else:
        content=f"ビートマップパック更新！\nhttps://osu.ppy.sh/beatmaps/packs\n{newPacksName}"

        webhookUrl = os.environ["WEBHOOK_URL"]
        payload={
            "content":content,
        }
        headers={"Content-Type": "application/json"}

        requests.post(webhookUrl,json.dumps(payload),headers=headers)