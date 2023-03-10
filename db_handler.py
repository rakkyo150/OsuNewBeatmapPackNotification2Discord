import os

def updateNewTopBeatmapPack(newDataPackId: str):
    with open('data.txt','w') as data:
        data.write(newDataPackId)

def exportOldTopBeatmapPack() -> str:
    id=''
    if not os.path.exists('data.txt'):
        return id
    with open('data.txt' ,'r') as data:
        id=data.readline()
        return id