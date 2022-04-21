import requests
from urllib import parse
from queue import PriorityQueue
class RiotApi:
    API_KEY = "API_KEY"
    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": API_KEY
    }
    PROFILE_RECENT_GAME_COUNT = 5
    MOST_CHAMPION_GAME_COUNT = 20

    def getUserInfo(self, userNickname):
        encodedName = parse.quote(userNickname)
        player = requests.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodedName,headers=self.REQUEST_HEADERS).json();
        return player;

    def getUserRankInfo(self, userNickname):
        lolUserInfoConsistOfJson = self.getUserInfo(userNickname);
        id = lolUserInfoConsistOfJson["id"];
        playerInfo = requests.get("https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+id, headers = self.REQUEST_HEADERS).json();
        return playerInfo

    def getUserLastGameId(self,puuid,gameCount):
        gameIdList = requests.get("https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?type=ranked&start=0&count="+str(gameCount), headers = self.REQUEST_HEADERS).json();
        return gameIdList;

    def getUserLastGames(self,userNickname):
        lolUserInfoConsistOfJson = self.getUserInfo(userNickname);
        puuid = lolUserInfoConsistOfJson["puuid"];
        userLastGameIdList = self.getUserLastGameId(puuid,self.PROFILE_RECENT_GAME_COUNT);
        gameList =[];
        for gameId in userLastGameIdList:
            gameInfo = requests.get("https://asia.api.riotgames.com/lol/match/v5/matches/"+gameId, headers = self.REQUEST_HEADERS).json();
            participantsList =gameInfo["info"]["participants"]
            for participant in participantsList:
                name = participant["summonerName"]
                if name==userNickname:
                    gameList.append(participant);
                    break;
        return gameList;

    def getMostChampion(self,userNickname):
        lolUserInfoConsistOfJson = self.getUserInfo(userNickname);
        puuid = lolUserInfoConsistOfJson["puuid"];
        userLastGameIdList = self.getUserLastGameId(puuid,self.MOST_CHAMPION_GAME_COUNT);
        que = PriorityQueue()
        championStat = {}
        for gameId in userLastGameIdList:
            gameInfo = requests.get("https://asia.api.riotgames.com/lol/match/v5/matches/" + gameId, headers=self.REQUEST_HEADERS).json();
            participantsList = gameInfo["info"]["participants"]
            for participant in participantsList:
                name = participant["summonerName"]
                if name==userNickname:
                    championName = participant["championName"]
                    nowKills = participant["kills"]
                    nowAssists = participant["assists"]
                    nowDeaths = participant["deaths"]
                    nowWinFlag = participant["win"]

                    if championName in championStat:
                        kills = championStat[championName]["kills"]
                        assists = championStat[championName]["assists"]
                        deaths = championStat[championName]["deaths"]
                        win = championStat[championName]["win"]
                        lose = championStat[championName]["lose"]

                        championStat[championName]["kills"] = kills + nowKills
                        championStat[championName]["assists"] = assists + nowAssists
                        championStat[championName]["deaths"] = deaths + nowDeaths
                        championStat[championName]["win"] = win + (1 if nowWinFlag else 0)
                        championStat[championName]["lose"] = lose + (0 if nowWinFlag else 1)
                    else:
                        gameStat = {
                            'name' : championName,
                            'kills' : nowKills,
                            'assists':nowAssists,
                            'deaths':nowDeaths,
                            'win':(1 if nowWinFlag else 0),
                            'lose':(0 if nowWinFlag else 1),
                        }
                        championStat[championName] = gameStat
                    break;
        maxCount = 0;
        maxKda = 0;
        mostChampion = {}
        for key in championStat.keys():
            champion = championStat[key];
            count = champion["win"]+champion["lose"]
            kda = (champion["kills"]+champion["assists"])/champion["deaths"]
            if maxCount<count:
                mostChampion = champion
                maxCount = count
                maxKda = kda
            elif maxCount == count and maxKda<kda:
                mostChampion = champion
                maxKda = kda
        return mostChampion

