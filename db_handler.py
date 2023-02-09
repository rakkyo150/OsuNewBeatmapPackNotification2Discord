import os

def updateNewBeatmapPack(newDataPackId):
    with open('data.txt','w') as data:
        data.write(newDataPackId)

def exportOldBeatmapPack():
    id=''
    if not os.path.exists('data.txt'):
        return id
    with open('data.txt' ,'r') as data:
        id=data.readline()
        return id