import requests as req
import json as js
import pandas as pd
import package.DbUtil as db
import package.Query as query
import time
import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

def creReviewTab():
    db.runQeury(query.getCreReviewQuery(), 'C', None)

def insReview(appList, gameListUrl): 
    for data in appList :
        total = 100                                             # variable to check if more reviews are needed
        cursor = '*'

        while(total == 100):                                    # to get more reviews(paging)
            reData = getReviewListr(data[0], gameListUrl, cursor)
            db.runQeury(query.getInsReviewListQuery(), 'I', reData['data'])
            #
            # create a while statement escape condition by checking the update date or creation date
            #
            cursor = reData['cursor']
            total = reData['total']
            

def getReviewListr(appid, gameListUrl, corsor):
    reqData = {
        "json" : 1,
        'filter' : 'recent',
        'language' : 'all',
        'cursor' : corsor, 
        'reivew_type' : 'all',
        'purchase_type' : 'all',
        'num_per_page' : 100
    }

    resData = req.post(gameListUrl+str(appid), params=reqData)
    # print(resData.url)                                         # show real url
    dataList = list()
    retData = {
        'total' : 0,
        'data' : None,
        'cursor' : None
    }
    
    if(resData.status_code == 200):
        textResReview = js.loads(resData.text) 
        print(textResReview['cursor'])

        if(textResReview['success'] == 1) :     
            retData['total'] = textResReview['query_summary']['total_reviews']
            # retData['cursor'] = textResReview['cursor']

            for data in textResReview['reviews']:
                dataList.append((appid, data['author']['steamid'], data['language'], changeTime(data['timestamp_created']), changeTime(data['timestamp_updated']),
                                'Y' if data['voted_up'] == True else 'N', 
                                'Y' if data['steam_purchase'] == True else 'N', 
                                'Y' if data['written_during_early_access'] == True else 'N'))
                # print(data['review'])                                     # review content analysis is planned during my master's studies
            retData['data'] = dataList
    else :
        logger.info("Failed to received review, appid: %s, cursor: %s", data[0], reqData['cursor'])
    return  retData

def changeTime(timestamp):
    return  datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')