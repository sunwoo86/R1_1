import requests as req
import json as js
import pandas as pd
import package.DbUtil as db
import package.Query as query
import time
import datetime

def insGameInfoList(ids, gameListUrl): 
    resList = list()

    for id in ids :
        reqData = {
            "appids" : id,
            'l' : 'korean' 
        }
        resData = req.post(gameListUrl, params=reqData)

        if(resData.status_code == 200) :
            appid = ''.join(reqData['appids'])                                         # list convert to string because json's first key is not supported list format
            if(resData.text == ''):
                resList = (None, None, '700', None, appid)                             # 700 : define(response is null)
            else :
                textResGameInfo = js.loads(resData.text)                                  
                if(textResGameInfo[appid]['success'] == False) :     
                    resList = (None, None, '800', None, appid)                         # 800 : define(response is failed)
                else :
                    print(appid, textResGameInfo[appid]['data']['release_date']['date'])
                    if(textResGameInfo[appid]['data']['release_date']['coming_soon'] == True):
                        comYn = "Y"
                        date = None
                    else:
                        comYn = "N"
                        date = convDateTime(textResGameInfo[appid]['data']['release_date']['date'])
                    resList = (textResGameInfo[appid]['data']['name'],
                            date,
                            resData.status_code,
                            comYn,
                            appid)
        else :
            resList = (None, None, str(resData.status_code), appid)                   # etc
        db.runQeury(query.getUpGameListQuery(), 'U', resList)
        time.sleep(2)                                                                 # prevent 429(Too Many Requests) 

def convDateTime(str):
    if(str == '') :
        return None
    else :
        splitStr = str.split('년')
        year = splitStr[0]
        if(splitStr[1] == ''):
            return None
        else :
            splitStr = splitStr[1].split('월')
            mon = splitStr[0]
            if(splitStr[1] == ''):
                day = 1
            else :
                day = splitStr[1].replace('일', '')
    return datetime.datetime(int(year), int(mon), int(day))

def getGameInfoList(beginDt, endDt):                      
    param = (datetime.datetime(int(beginDt[0:4]), int(beginDt[4:6]), int(beginDt[6:])), # begin date 
             datetime.datetime(int(endDt[0:4]), int(endDt[4:6]), int(endDt[6:])))        # end date

    return db.runQeury(query.getSelGameInfoListQuery(), 'S', param)


    