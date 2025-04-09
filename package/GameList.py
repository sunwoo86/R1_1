import requests as req
import json as js
import pandas as pd
import package.DbUtil as db
import package.Query as query
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

def creGameInfoTab():
    db.runQeury(query.getCreGameInfoQuery(), 'C', None)

def insGameList(self, gameListUrl): 
    resGameList = req.get(gameListUrl)

    if(resGameList.status_code == 200):
        textGameList= js.loads(resGameList.text)
        datasGameList = textGameList['applist']['apps']
        gamelist = list()
        for data in datasGameList:
            gamelist.append((str(data['appid']), "200"))
            # gamelist.append((data['appid'], data['name']), '200')    #pymysql.err.DataError: (1366, "Incorrect string value: '\\xF0\\x9F\\x92\\x9D' for column 'name' at row 1")
        db.runQeury(query.getInsGameListQuery(), 'I', gamelist)
    else:
        logging.info(resGameList.status_code)

def getGameList():
    return db.runQeury(query.getGameListQuery(), 'S', None)

    
