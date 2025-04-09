import sys
import os
sys.path.append(os.path.abspath(os.path.dirname('info')))
from info import dbInfo
import pandas as pd
import pymysql
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

def getConn(attempts=3, delay=2):
    info = dbInfo._dbInfo 
    attempt = 1

    while attempt < attempts + 1:
        try:
            return pymysql.connect(
                db = info['db'],   
                host = info['host'],     
                user = info['user'],     
                passwd = info['password'], 
                port = info['port'],       
                charset =  info['charset'])
        except (pymysql.connect.Error, IOError) as err:
            if (attempts is attempt):
                # Attempts to reconnect failed; returning None
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts-1,
            )
            # progressive reconnect delay
            time.sleep(delay ** attempt)
            attempt += 1
    return None

def runQeury(query, div, dataList):
    con = getConn()
    cur = con.cursor()
    result = None

    match div:
        case 'C': cur.execute(query)
        case 'I': 
            for data in dataList :
                cur.execute(query, data)  
                print(cur._executed)
        case 'S':
            cur.execute(query, dataList)
            # print(cur._executed)                                          # show real query
            result = cur.fetchall()
            result = [list(result[item]) for item in range(len(result))]
            # result = pd.DataFrame(result)
        case 'U': 
            cur.execute(query, dataList)
    con.commit()
    cur.close()
    con.close()
    return result