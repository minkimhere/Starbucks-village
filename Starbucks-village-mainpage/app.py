from pymongo import MongoClient
from bson import ObjectId
import jwt
import hashlib
import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

client = MongoClient('localhost', 27017)
db = client.starbucksVillage


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload["id"]})
        reviews = list(db.reviews.find({}))
        for review in reviews:
            review["review_id"] = str(review["_id"])
            review["heart_by_me"] = bool(db.likes.find_one({"review_id": review["review_id"], "id": payload['id']}))
            print(review)
        return render_template('main.html', user_info=user_info, reviews=reviews)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/mypage')
def mypage():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})
    nickname = user_info['nickname']

    reviews = list(db.reviews.find({"nickname": nickname}))
    for review in reviews:
        review["review_id"] = str(review["_id"])
        review["heart_by_me"] = bool(db.likes.find_one({"review_id": review["review_id"], "id": payload['id']}))

    return render_template('myPage.html', nickname=nickname, reviews=reviews)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": username_receive,
        "password": password_hash,
        "nickname": username_receive,
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/api/category', methods=['POST'])
def review_category():
    select_receive = request.form['select_give']
    coffees = list(db.coffees.find({'category': select_receive}, {'_id': False}))

    print(coffees)

    return jsonify({'all_coffees': coffees})


@app.route('/api/write', methods=['POST'])
def review_write():
    category_receive = request.form['category_give']
    coffeename_receive = request.form['coffeeName_give']
    starrating_receive = request.form['starRating_give']
    reviewcontent_receive = request.form['review_give']

    image = db.coffees.find_one({'coffeeName': coffeename_receive}, {'_id': False})

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})
    nickname = user_info['nickname']

    doc = {
        'image': image["image"],
        'category': category_receive,
        'coffeeName': coffeename_receive,
        'starRating': starrating_receive,
        'review': reviewcontent_receive,
        'nickname': nickname,
        'Like':0
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': f'{nickname}님의 리뷰 작성이 완료되었습니다!'})

@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 좋아요 수 변경
        user_info = db.users.find_one({"id": payload["id"]})
        review_id_receive = request.form["review_id_give"]
        action_receive = request.form["action_give"]
        now_review = db.reviews.find_one({'_id': ObjectId(review_id_receive)})
        now_like = now_review['Like']
        doc = {
            "review_id": review_id_receive,
            "id": user_info["id"],
        }
        if action_receive == "like":
            db.likes.insert_one(doc)
            db.reviews.update_one({'_id': ObjectId(review_id_receive)},{'$set':{'Like':now_like+1}})
        else:
            db.likes.delete_one(doc)
            db.reviews.update_one({'_id': ObjectId(review_id_receive)}, {'$set': {'Like': now_like-1}})
        result_like = db.reviews.find_one({'_id': ObjectId(review_id_receive)},{'_id':False})
        return jsonify({"result": "success", 'msg': 'updated', 'result_like': result_like})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/api/delete_review', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    review_recive = request.form["review_give"]

    db.reviews.delete_one({"review": review_recive})

    return jsonify({'result': 'success', 'msg': '리뷰 삭제'})

@app.route('/api/modal', methods=['POST'])
def card_modal():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})
    id_receive = request.form["id_give"]

    review = db.reviews.find_one({"_id": ObjectId(id_receive)})
    delete_auth = bool(user_info['nickname'] == review['nickname'])
    print(review)
    review["_id"] = str(review["_id"])
    review["heart_by_me"] = bool(db.likes.find_one({"review_id": review["_id"], "id": payload['id']}))

    return jsonify({'card': review, 'delete_auth': delete_auth})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)