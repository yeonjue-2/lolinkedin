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

    riotData = riotapi.RiotApi()

    for user in userinput:
        userData = {}
        userData['userData'] = riotData.getUserRankInfo(user['userName'])
        userData['userName'] = user['userName']
        userDataList.append(userData);

    return jsonify(userDataList)


@app.route('/api/member', methods=['GET'])
def userInfo():

    userName = request.args.get('userName')

    riotData = riotapi.RiotApi()

    userData = riotData.getUserRankInfo(userName)
    tier = userData[0]['tier']
    rank = userData[0]['rank']

    lastGames = riotData.getUserLastGames(userName)

    return jsonify({'tier':tier, 'rank':rank, 'lastGames':lastGames})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
