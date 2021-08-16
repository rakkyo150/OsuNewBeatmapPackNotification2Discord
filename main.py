import requests
from bs4 import BeautifulSoup
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

import db_handler

link="https://osu.ppy.sh/beatmaps/packs"

options=Options()
options.add_argument("--headless")

driver=webdriver.Chrome(executable_path=os.environ["CHROME_DRIVER"],options=options)
# 暗黙的待機
driver.implicitly_wait(10)
wait=WebDriverWait(driver,30)

driver.get(link)
wait.until(EC.presence_of_all_elements_located)

collapse=driver.find_element_by_class_name("fa-chevron-down")
collapse.click()
wait.until(EC.presence_of_all_elements_located)

loginPopup=driver.find_element_by_class_name("avatar")
loginPopup.click()
wait.until(EC.presence_of_all_elements_located)

username=driver.find_element_by_name("username")
username.send_keys(os.environ["USER_NAME"])

password=driver.find_element_by_name("password")
password.send_keys(os.environ["PASSWORD"])

loginButton=driver.find_element_by_class_name("fa-sign-in-alt")
loginButton.click()
wait.until(EC.presence_of_all_elements_located)
# ブラウザのログイン処理待ち
sleep(3)

response=driver.page_source.encode("utf-8")
soup=BeautifulSoup(response,"html.parser")
packList=soup.find("div",class_="js-accordion")
topPackDiv=packList.div

topDataPackId=topPackDiv.get("data-pack-id")
topPackName=topPackDiv.a.div.text

avoidWord=["taiko","catch","mania"]

oldDataPackId=db_handler.exportOldBeatmapPack()

# 初回
if oldDataPackId is None:
    packDivs = packList.find_all("div", class_="beatmap-pack")
    for pack in packDivs:
        packName = pack.a.div.text

        if any(words in packName.lower() for words in avoidWord):
            pass
        else:
            packContentLink=pack.a.get("href")
            driver.get(packContentLink)
            packContentHtml=driver.page_source.encode("utf-8")
            packContentSoup=BeautifulSoup(packContentHtml,"html.parser")
            packDownloadA=packContentSoup.find("a",class_="beatmap-pack-download__link")

            content="**初実行！**\nhttps://osu.ppy.sh/beatmaps/packs"
            description="**"+packName+"**\n"+packDownloadA.get("href")

            webhookUrl = os.environ["WEBHOOK_URL"]
            payload = {
                "content": content,
                "embeds": [{
                    "description": description,
                    "color":15753632
                }],
            }
            headers = {"Content-Type": "application/json"}

            requests.post(webhookUrl, json.dumps(payload), headers=headers)

            break
    db_handler.updateNewBeatmapPack("firstExecution", topDataPackId)

# 更新してるかどうか
elif oldDataPackId==topDataPackId:
    pass
else:
    description=""
    newPack=False
    packDivs=packList.find_all("div",class_="beatmap-pack")
    for pack in packDivs:
        # 直近の更新までループが終わったとき
        if str(pack.get("data-pack-id"))==oldDataPackId:
            # 更新あったとき
            if newPack is True:
                db_handler.updateNewBeatmapPack(oldDataPackId, topDataPackId)
            break
        else:
            newPack=True
            # 更新内容をosu!stdとそれ以外で分けてnewPacksNameを作る
            packName=pack.a.div.text
            if any(words in packName.lower() for words in avoidWord):
                pass
            else:
                packContentLink = pack.a.get("href")
                driver.get(packContentLink)
                packContentHtml = driver.page_source.encode("utf-8")
                packContentSoup = BeautifulSoup(packContentHtml, "html.parser")
                packDownloadA = packContentSoup.find("a",class_="beatmap-pack-download__link")

                description+="**"+packName+"**\n"+packDownloadA.get("href")+"\n"

    # 更新内容がosu!std以外しかないorそもそも更新していない場合はディスコートに通知しない
    if description=="":
        pass
    else:
        content=f"**ビートマップパック更新！**\nhttps://osu.ppy.sh/beatmaps/packs\n"

        webhookUrl = os.environ["WEBHOOK_URL"]
        payload={
            "content":content,
            "embeds":[{
                "description":description,
                "color": 15753632
            }],
        }
        headers={"Content-Type": "application/json"}

        requests.post(webhookUrl,json.dumps(payload),headers=headers)

driver.close()