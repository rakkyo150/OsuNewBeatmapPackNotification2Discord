#!/bin/sh

echo Please input WEBHOOK_URL
read WEBHOOK_URL
# echo Please input osu! USER_NAME
# read USER_NAME
# echo Please input osu! PASSWORD
# read PASSWORD

echo "WEBHOOK_URL=$WEBHOOK_URL">>.env

sudo apt install chromium-chromedriver

uv sync
uv run main.py

echo Finish!