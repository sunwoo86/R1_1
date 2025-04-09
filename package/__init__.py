_gameListUrl = "https://api.steampowered.com/ISteamApps/GetAppList/v2"
_gameInfoUrl = "https://store.steampowered.com/api/appdetails"
_reviewUrl = "https://store.steampowered.com/appreviews/"
_headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}

def getGameListUrl():
    return _gameListUrl

def getGameInfoUrl():
    return _gameInfoUrl

def getReviewUrl():
    return _reviewUrl