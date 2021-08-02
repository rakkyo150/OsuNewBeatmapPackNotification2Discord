import psycopg2
import os



def upsertNewBeatmapPack(oldDataPackId,newDataPackId):
    link=os.environ["DATABASE_URL"]
    con=psycopg2.connect(link)
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS osuNewBeatmapPack(dataPackId TEXT)")
    cur.execute("DELETE FROM osuNewBeatmapPack WHERE title=%s",(oldDataPackId,))
    cur.execute("INSERT INTO osuNewBeatmapPack (title) VALUES (%s)",(newDataPackId,))
    con.commit()
    con.close()

def exportOldBeatmapPack():
    link = os.environ["DATABASE_URL"]
    con = psycopg2.connect(link)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS osuNewBeatmapPack(title TEXT)")
    cur.execute("SELECT * FROM osuNewBeatmapPack")
    oldDataPackId=cur.fetchone()
    con.commit()
    con.close()
    return oldDataPackId[0]