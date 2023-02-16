#!/bin/sh

echo Please input WEBHOOK_URL
read WEBHOOK_URL
echo Please input osu! USER_NAME
read USER_NAME
echo Please input osu! PASSWORD
read PASSWORD

echo "WEBHOOK_URL=$WEBHOOK_URL
USER_NAME=$USER_NAME
PASSWORD=$PASSWORD">>.env

sudo apt install chromium-chromedriver

python -m venv venv
venv/bin/python -m pip install -r requirements.txt

venv/bin/python main.py

echo Finish!