$(document).ready(function () {
    showUserInfo();
});

function showUserInfo() {

    urlSearch = new URLSearchParams(location.search);
    userName = urlSearch.get('userName')

    $.ajax({
        type: 'GET',
        url: '/api/member?userName=' + userName,
        data: {},
        success: function (response) {
            let tier = response['tier']
            let rank = response['rank']
            let lastGames = response['lastGames']
            let mostChampions = response['mostChampions']
            let mostChampName = mostChampions['name']
            let mostChampWin = mostChampions['win']
            let mostChampLose = mostChampions['lose']
            let allGames = mostChampWin + mostChampLose
            let mostChampKills = mostChampions['kills']
            let avKills = (mostChampKills / allGames).toFixed(1)
            let mostChampDeaths = mostChampions['deaths']
            let avDeaths = (mostChampDeaths / allGames).toFixed(1)
            let mostChampAssists = mostChampions['assists']
            let avAssist = (mostChampAssists / allGames).toFixed(1)
            let average = ((mostChampKills + mostChampAssists) / mostChampDeaths).toFixed(2)

            $('#summonerName').html(userName)
            $('#tier').html(tier)
            $('#rank').html(rank)
            $('#mostChampionName').html(mostChampName)
            $('#all').html(allGames)
            $('#win').html(mostChampWin)
            $('#lose').html(mostChampLose)
            $('#kill').html(avKills)
            $('#death').html(avDeaths)
            $('#assist').html(avAssist)
            $('#average').html(average)

            for (let i = 0; i < lastGames.length; i++) {
                let summonerName = lastGames[i]['summonerName']
                let championName = lastGames[i]['championName']
                let teamPosition = lastGames[i]['teamPosition']
                let kills = lastGames[i]['kills']
                let deaths = lastGames[i]['deaths']
                let assists = lastGames[i][`assists`]
                let win = lastGames[i]['win']
                let gameResult

                if (win == true) {
                    gameResult = "승리"
                } else {
                    gameResult = "패배"
                }
                let totalMinionsKilled = lastGames[i]['totalMinionsKilled']
                let timePlayed = lastGames[i]['timePlayed']
                let minutes = parseInt(timePlayed / 60)
                let seconds = timePlayed % 60

                let temp_html = `<li>
                                            <div class="logBox-css">
                                                <div class="info">
                                                    <div class="game-result">${gameResult}</div>
                                                    <div class="bar"></div>
                                                    <div class="game-length">${minutes}분 ${seconds}초</div>
                                                </div>
                                                <div class="position">
                                                    <div class="icon">
                                                        <img src="../static/image/${teamPosition}.png" alt="포지션아이콘">
                                                    </div>
                                                    <div class="name">${teamPosition}</div>
                                                </div>
                                                <div class="champion">
                                                    <div class="icon">
                                                        <img src="../static/image/ari.png" alt="챔피언사진">
                                                    </div>
                                                    <div class="name">${championName}</div>
                                                </div>
                                                <div class="kda">
                                                    <div class="k-d-a">
                                                        <span>${kills}</span>
                                                        /
                                                        <span style="color: red">${deaths}</span>
                                                        /
                                                        <span>${assists}</span>
                                                    </div>
                                                    <div class="status">cs ${totalMinionsKilled}</div>
                                                </div>
                                            </div>
                                        </li>`
                $('#gameData').append(temp_html)

                if (win == false) {
                    document.getElementsByClassName('logBox-css')[i].style.backgroundColor = 'MistyRose'
                    document.getElementsByClassName('game-result')[i].style.color = 'red'
                }
            }
        }
    });
}
