from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

import riotapi

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbchallenger

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/userinfo')
def showUserInfo():
    return render_template('userInfo.html')

@app.route('/mainpage')
def showmain():
    return render_template('mainpage.html')


@app.route('/api/mainpage', methods=['GET'])
def user_nick():
    userinput = list(db.users.find())

    userDataList = []



    for user in userinput:
        userData = {}
        riotData = riotapi.RiotApi(user['userName'])
        userData['userData'] = riotData.getUserRankInfo()
        userData['userName'] = user['userName']
        userDataList.append(userData);

    return jsonify({'userDataList':userDataList})



@app.route('/api/member', methods=['GET'])
def userInfo():

    userName = request.args.get('userName')
    riotData = riotapi.RiotApi(userName)

    userData = riotData.getUserRankInfo()
    tier = userData[0]['tier']
    rank = userData[0]['rank']

    riots = riotData.getUserLastGameInfo()
    lastGames = riots['gameInfo']
    mostChampions = riots['mostChampionStat']

    return jsonify({'tier':tier, 'rank':rank, 'lastGames':lastGames, 'mostChampions':mostChampions})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
