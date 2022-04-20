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

@app.route('/api/member', methods=['GET'])
def userInfo(userName):

    userName = request.form['userName_give']    ## 누를 때 userName 받아오기..?

    riotData = riotapi.RiotApi()

    userData = riotData.getUserRankInfo(userName)      #티어
    tier = userData['tier']
    rank = userData['rank']

    lastGames = riotData.getUserLastGames(userName)    #최근전적

    return jsonify({'tier':tier, 'rank':rank, 'lastGames':lastGames})









if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
