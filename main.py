import package as pack
import package.GameList as getList
import package.GameInfo as getInfo
import package.Review as getRev
import datetime

beginDt = '20230101'
endDt = '20231231'

# getList.creGameInfoTab()                                                # create gameInfo table
# getList.insGameList('list', pack.getGameListUrl())                      # get gameList from Steam site and isnert into db

#getInfo.insGameInfoList(getList.getGameList(), pack.getGameInfoUrl())   # get infomation in gameList and update to db

# getRev.creReviewTab()                                                     # create reviewInfo table
getRev.insReview(getInfo.getGameInfoList(beginDt, endDt), pack.getReviewUrl())  #  get review and insert into db




