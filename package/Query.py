_creGameInfoQuery =  '''CREATE TABLE IF NOT EXISTS GAME_DB.GAME_INFO(                             # GameInfo DB
                          appid  VARCHAR(10) PRIMARY KEY,                                         # steam game ID
                          name   VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,   # game title
                          relDt  date,                                                            # release date
                          inDt   datetime,                                                        # input time
                          upDt   datetime,                                                        # update time
                          errCd  VARCHAR(3),                                                      # http response code 
                          comYn  VARCHAR(1)                                                       # comming soon or not
                    )'''

_insGameListQuery =  '''INSERT INTO GAME_DB.GAME_INFO(
                            appid,
                            name,
                            relDt,
                            inDt,
                            upDt,
                            errCd,
                            comYn
                        ) VALUES (
                            %s,
                            NULL,                                                                 # Some game's titles occur charset-error
                            NULL,
                            now(),
                            now(),
                            %s,
                            NULL
                        )
                        ON DUPLICATE KEY UPDATE
                            upDt = now()
                    '''

_selGameListQuery = "SELECT appid FROM GAME_DB.GAME_INFO WHERE name IS NULL AND errCd = '200'"
# _selGameListQuery = "SELECT appid FROM GAME_DB.GAME_INFO WHERE appid = '1091400'"

_upGameList =  '''UPDATE GAME_DB.GAME_INFO SET 
                    name = %s,
                    relDt = %s,
                    upDt = now(),
                    errCd = %s,
                    comYn = %s
                  WHERE appid = %s
                '''

# _selGameInfoListQuery = '''SELECT appid, relDt FROM GAME_DB.GAME_INFO 
#                             WHERE relDt BETWEEN %s AND %s
#                         '''

_selGameInfoListQuery = '''SELECT appid, relDt FROM GAME_DB.GAME_INFO 
                            WHERE relDt BETWEEN %s AND %s
                            LIMIT 2
                        '''

_creReviewQuery =  '''CREATE TABLE IF NOT EXISTS GAME_DB.REVIEW_INFO(                            # REVIEW_INFO DB
                        appid   VARCHAR(10),                                                     # steam game ID
                        userid  VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,   # user ID
                        langage VARCHAR(30),                                                     # review language
                        reCreDt date,                                                            # review creation date
                        reUpDt  date,                                                            # review update date  
                        recoYn  VARCHAR(1),                                                      # recommended or not
                        purYn   VARCHAR(1),                                                      # purchase or not
                        ealYn   VARCHAR(1),                                                      # early access or not
                        inDt    datetime,                                                        # input time
                        upDt    datetime,                                                        # update time
                        UNIQUE KEY uni_review(appid, userid)
                    )'''

_insReviewListQuery =  '''INSERT INTO GAME_DB.REVIEW_INFO(
                            appid,
                            userid,
                            langage,
                            reCreDt,
                            reUpDt,
                            recoYn,
                            purYn,
                            ealYn,
                            inDt,
                            upDt
                        ) VALUES (
                            %s,
                            %s,                                                                 
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            now(),
                            now()
                        )
                        ON DUPLICATE KEY UPDATE
                            upDt = now()
                    '''

def getCreGameInfoQuery():
    return _creGameInfoQuery

def getInsGameListQuery():
    return _insGameListQuery

def getGameListQuery():
    return _selGameListQuery

def getUpGameListQuery():
    return _upGameList

def getSelGameInfoListQuery():
    return _selGameInfoListQuery

def getCreReviewQuery():
    return _creReviewQuery

def getInsReviewListQuery():
    return _insReviewListQuery