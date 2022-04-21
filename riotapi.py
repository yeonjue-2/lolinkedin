import requests
from urllib import parse

class RiotApi:
    def __init__(self,userNickname):
        encodedName = parse.quote(userNickname)
        player = requests.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodedName, headers=self.REQUEST_HEADERS).json();
        self.userNickname = userNickname
        self.lolUserInfoConsistOfJson = player
        self.gameList = []
        self.championStat = {}
    API_KEY = "API_KEY"
    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": API_KEY
    }
    USER_LAST_GAME_COUNT = 20

    def getUserRankInfo(self):
        id = self.lolUserInfoConsistOfJson["id"];
        playerInfo = requests.get("https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+id, headers = self.REQUEST_HEADERS).json();
        return playerInfo

    def getUserLastGameId(self,puuid,gameCount):
        gameIdList = requests.get("https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?type=ranked&start=0&count="+str(gameCount), headers = self.REQUEST_HEADERS).json();
        return gameIdList;

    def getUserLastGameInfo(self):
        puuid = self.lolUserInfoConsistOfJson["puuid"];
        userLastGameIdList = self.getUserLastGameId(puuid,self.USER_LAST_GAME_COUNT);

        for gameId in userLastGameIdList:
            gameInfo = requests.get("https://asia.api.riotgames.com/lol/match/v5/matches/"+gameId, headers = self.REQUEST_HEADERS).json();
            participantsList =gameInfo["info"]["participants"]
            for participant in participantsList:
                name = participant["summonerName"]
                if name==self.userNickname:
                    self.gameList.append(participant);
                    break;
        mostChampionStat = self.getMostChampion();
        return {'gameInfo':self.gameList,'mostChampionStat':mostChampionStat};

    def getMostChampion(self):
        for game in self.gameList:
            championName = game["championName"]
            nowKills = game["kills"]
            nowAssists = game["assists"]
            nowDeaths = game["deaths"]
            nowWinFlag = game["win"]

            if championName in self.championStat:
                kills = self.championStat[championName]["kills"]
                assists = self.championStat[championName]["assists"]
                deaths = self.championStat[championName]["deaths"]
                win = self.championStat[championName]["win"]
                lose = self.championStat[championName]["lose"]

                self.championStat[championName]["kills"] = kills + nowKills
                self.championStat[championName]["assists"] = assists + nowAssists
                self.championStat[championName]["deaths"] = deaths + nowDeaths
                self.championStat[championName]["win"] = win + (1 if nowWinFlag else 0)
                self.championStat[championName]["lose"] = lose + (0 if nowWinFlag else 1)
            else:
                gameStat = {
                    'name' : championName,
                    'kills' : nowKills,
                    'assists':nowAssists,
                    'deaths':nowDeaths,
                    'win':(1 if nowWinFlag else 0),
                    'lose':(0 if nowWinFlag else 1),
                }
                self.championStat[championName] = gameStat
            break;

        maxCount = 0;
        maxKda = 0;
        mostChampion = {}
        for key in self.championStat.keys():
            champion = self.championStat[key];
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
