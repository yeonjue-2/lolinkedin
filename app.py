from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

import riotapi

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbchallenger


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/userinfo')
def showUserInfo():
    return render_template('userInfo.html')

# userinfo 페이지에 데이터 전송
@app.route('/api/member', methods=['GET'])
def userInfo():

    userName = request.args.get('userName')

    riotData = riotapi.RiotApi()

    userData = riotData.getUserRankInfo(userName)
    tier = userData[0]['tier']
    rank = userData[0]['rank']

    lastGames = riotData.getUserLastGames(userName)

    mostChampions = riotData.getMostChampion(userName)

    return jsonify({'tier':tier, 'rank':rank, 'lastGames':lastGames, 'mostChampions':mostChampions})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
