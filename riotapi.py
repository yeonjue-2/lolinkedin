import requests
from urllib import parse

class RiotApi:
    API_KEY = "API_KEY"
    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": API_KEY
    }

    def getUserInfo(self, userNickname):
        encodedName = parse.quote(userNickname)
        player = requests.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodedName,headers=self.REQUEST_HEADERS).json();
        return player;

    def getUserRankInfo(self, userNickname):
        lolUserInfoConsistOfJson = self.getUserInfo(userNickname);
        id = lolUserInfoConsistOfJson["id"];
        playerInfo = requests.get("https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+id, headers = self.REQUEST_HEADERS).json();
        return playerInfo

    def getUserLastGameId(self,puuid):
        gameIdList = requests.get("https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?type=ranked&start=0&count=5", headers = self.REQUEST_HEADERS).json();
        return gameIdList;

    def getUserLastGames(self,userNickname):
        lolUserInfoConsistOfJson = self.getUserInfo(userNickname);
        puuid = lolUserInfoConsistOfJson["puuid"];
        userLastGameIdList = self.getUserLastGameId(puuid);
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