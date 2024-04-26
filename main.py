import requests
from bs4 import BeautifulSoup
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep

import db_handler


from dotenv import load_dotenv
load_dotenv()

def login_to_osu(driver, wait):
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
    
def get_pack_list_info(driver):
    response = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(response, "html.parser")
    packList = soup.find("div", class_="js-accordion")
    topPackDiv = packList.div

    topDataPackTag: str = topPackDiv.get("data-pack-tag")
    topPackName = topPackDiv.find(class_="beatmap-pack__name").text

    return packList, topDataPackTag, topPackName

def get_pack_download_a(driver, pack):
    packContentLink = pack.a.get("href")
    driver.get(packContentLink)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"beatmap-pack-download__link")))
    packContentHtml = driver.page_source.encode("utf-8")
    packContentSoup = BeautifulSoup(packContentHtml, "html.parser")
    packDownloadA = packContentSoup.find("a",class_="beatmap-pack-download__link")
    return packDownloadA

def send_notification(content, description):
    webhookUrl = os.environ["WEBHOOK_URL"]
    payload = {
        "content": content,
        "embeds": [{
            "description": description,
            "color":15753632
        }],
    }
    headers={"Content-Type": "application/json"}
    requests.post(webhookUrl,json.dumps(payload),headers=headers)

options=Options()
options.add_argument("--headless")

# driver=webdriver.Chrome(executable_path=os.environ["CHROME_DRIVER"],options=options)
driver=webdriver.Chrome(options=options)

# 暗黙的待機
driver.implicitly_wait(10)
wait=WebDriverWait(driver,30)

try:
    link="https://osu.ppy.sh/beatmaps/packs"
    avoidWord=["taiko","catch","mania"]

    driver.get(link)
    wait.until(EC.presence_of_all_elements_located)

    login_to_osu(driver, wait)

    packList, topDataPackTag, topPackName = get_pack_list_info(driver)

    # oldDataPackId='for test'
    oldTopDataPackTag=db_handler.exportOldTopBeatmapPack()
    print(oldTopDataPackTag)

    # 初回
    if oldTopDataPackTag=='':
        packDivs = packList.find_all("div", class_="beatmap-pack")
        for pack in packDivs:
            packName: str = pack.find(class_="beatmap-pack__name").text

            if any(words in packName.lower() for words in avoidWord):
                pass
            else:
                packDownloadA = get_pack_download_a(driver, pack)

                content="**初実行！**\nhttps://osu.ppy.sh/beatmaps/packs"
                description="**"+packName+"**\n"+packDownloadA.get("href")
                send_notification(content, description)

                break
        db_handler.updateNewTopBeatmapPack(topDataPackTag)

    # 更新してるかどうか
    elif oldTopDataPackTag==topDataPackTag:
        pass
    else:
        description=""
        newPack=False
        packDivs=packList.find_all("div",class_="beatmap-pack")
        for pack in packDivs:
            # 直近の更新までループが終わったとき
            if str(pack.get("data-pack-tag"))==oldTopDataPackTag:
                db_handler.updateNewTopBeatmapPack(topDataPackTag)
                break

            newPack=True
            # 更新内容をosu!stdとそれ以外で分けてnewPacksNameを作る
            packName=pack.find(class_="beatmap-pack__name").text
            if any(words in packName.lower() for words in avoidWord):
                pass
            else:
                packDownloadA = get_pack_download_a(driver, pack)

                description+="**"+packName+"**\n"+packDownloadA.get("href")+"\n"
                
            # ページを越えないと更新においつけない場合でも最新のデータに更新を忘れないこと
            if pack == packDivs[-1]:
                db_handler.updateNewTopBeatmapPack(topDataPackTag)

        # 更新内容がosu!std以外しかないorそもそも更新していない場合はディスコートに通知しない
        if description=="":
            pass
        else:
            content=f"@everyone\n**ビートマップパック更新！**\nhttps://osu.ppy.sh/beatmaps/packs\n"
            send_notification(content, description)

    driver.quit()
except Exception as e:
    print(e.__class__.__name__)
    print(e.args)
    print(e)
    print(f"{e.__class__.__name__}: {e}")
    driver.quit()