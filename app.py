from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request , session

import riotapi

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbchallenger

@app.route('/')
def home():
    return render_template('mainpage.html')

@app.route('/userinfo')
def showUserInfo():
    return render_template('userInfo.html')

@app.route('/mainpage')
def showmain():
    return render_template('mainpage.html')


@app.route('/api/mainpage', methods=['GET'])
def user_nick():
    userinput = list(db.members.find())

    userDataList = []

    for user in userinput:
        userData = {}
        riotData = riotapi.RiotApi(user['summersName'])
        userData['userData'] = riotData.getUserRankInfo()
        userData['userName'] = user['summersName']
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

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template("login.html")
    else:
        userId = request.form.get('userId')
        password = request.form.get('password')

        if not (userId and password ):
            return jsonify({'msg': '모두 입력해주세요!'})

        user = db.dbchallenger.find_one({"userId": userId, "password": password}, {"name", "email", "summersName"})
        counting = db.dbchallenger.find_one({"userId": userId, "password": password})

        if counting == None:
            return jsonify({'msg': '아이디와 비밀번호를 확인해주세요.'})

        else:

            # session['userInfo'] = user

            return jsonify({'msg': '로그인 되었습니다!'})










@app.route('/register', methods=['GET','POST'])
def register():


    if request.method == 'GET':
        return render_template("register.html")
    else:

        userId = request.form.get('userId')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')
        summersName = request.form.get('summersName')

        if not (userId and password and name and email and summersName):
            return jsonify({'msg': '모두 입력해주세요!'})

        else: doc = {
            'userId': userId,
            'password': password,
            'name': name,
            'email': email,
            'summersName': summersName
        }

        db.dbchallenger.insert_one(doc)


    return jsonify({'msg': '회원가입 완료! 환영합니다!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
