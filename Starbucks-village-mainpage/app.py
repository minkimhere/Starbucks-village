from pymongo import MongoClient
from bson import ObjectId
import jwt
import hashlib
import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# jwt 토큰을 디코드하기위한 KEY
SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb://15.165.204.201', 27017, username="test", password="test")
# client = MongoClient('localhost', 27017)
db = client.starbucksVillage


# 메인 페이지로 정보 전달
@app.route('/')
def home():
    # 쿠키에 저장되어 있는 jwt 토큰을 받아옴
    token_receive = request.cookies.get('mytoken')
    try:
        # jwt 토큰을 디코드 하여 payload에 저장
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # 로그인 된 유저의 id를 user_info에 저장
        user_info = db.users.find_one({"id": payload["id"]})

        # db에서 reviews의 정보들을 reviews에 저장
        reviews = list(db.reviews.find({}))
        # 가장 마지막에 저장된 리뷰가 가장 앞에서 보여지도록 순서를 뒤집음
        reviews.reverse()
        for review in reviews:
            # db에 있는 review id를 str 형을 보내주기 위해 형 변환
            review["review_id"] = str(review["_id"])
            # 로그인된 유저의 id 정보로 review의 좋아요를 눌렀는지 확인하여 bool 형으로 저장
            review["heart_by_me"] = bool(db.likes.find_one({"review_id": review["review_id"], "id": payload['id']}))
            print(review)

        # 메인 페이지를 그릴 때, user_info와 reviews를 보내줌
        return render_template('main.html', user_info=user_info, reviews=reviews)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 로그인 페이지 이동
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# 마이 페이지로 정보 전달
@app.route('/mypage')
def mypage():
    # def home() 과 동일
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})
    ###

    # user_info에 저장된 유저 정보중 nickname을 따로 저장
    nickname = user_info['nickname']

    # 리뷰중 로그인된 유저의 nickname 과 일치하하는 리뷰만 가져와 저장
    reviews = list(db.reviews.find({"nickname": nickname}))
    # 가장 마지막에 저장된 리뷰가 가장 앞에서 보여지도록 순서를 뒤집음
    reviews.reverse()
    for review in reviews:
        review["review_id"] = str(review["_id"])
        review["heart_by_me"] = bool(db.likes.find_one({"review_id": review["review_id"], "id": payload['id']}))

    # 메인 페이지를 그릴 때, user_info와 reviews를 보내줌
    return render_template('myPage.html', nickname=nickname, reviews=reviews)


# 로그인 완료
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 사용자가 작성한 id, password를 받아 저장
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # hash 형태로 인코드하여 비밀번호 저장
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    
    # db users에 사용자가 입력한 id, password가 일치하는 것이 있는지 확인
    result = db.users.find_one({'id': username_receive, 'password': pw_hash})

    # 결과가 일치한다면,
    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        # jwt토큰 생성
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 사용자가 작성한 id, password를 받아 저장
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    
    # hash 형태로 인코드하여 비밀번호 저장
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    
    # 입력한 정보를 토대로 doc 생성
    doc = {
        "id": username_receive,
        "password": password_hash,
        "nickname": username_receive,
    }
    
    # doc을 db users에 저장
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 회원가입 아이디 중복 체크
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # 사용자가 작성한 id를 받아 저장
    username_receive = request.form['username_give']
    
    # 사용자가 작성한 id가 이미 db users에 있는지 확인하여 bool 형태로 저장
    exists = bool(db.users.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 선택된 음료 카테고리안에 있는 음료의 정보들을 보내줌
@app.route('/api/category', methods=['POST'])
def review_category():
    # 사용자가 선택한 음료의 카테고리를 받아서 select_receive에 저장
    select_receive = request.form['select_give']
    
    # 선택된 카테고리 안에 있는 음료 정보를 db coffees에서 찾아 저장
    coffees = list(db.coffees.find({'category': select_receive}, {'_id': False}))

    print(coffees)

    # 화면에 그리기 위해 저장된 coffees의 정보를 보내줌
    return jsonify({'all_coffees': coffees})


# 사용자가 작성한 리뷰를 db에 저장
@app.route('/api/write', methods=['POST'])
def review_write():
    # 사용자가 직접 선택한 카테고리, 커피 이름, 평점, 리뷰 내용을 받아옴
    category_receive = request.form['category_give']
    coffeename_receive = request.form['coffeeName_give']
    starrating_receive = request.form['starRating_give']
    reviewcontent_receive = request.form['review_give']

    # db coffees에서 사용자가 선택한 커피 이름과 일치하는 음료의 정보를 저장
    image = db.coffees.find_one({'coffeeName': coffeename_receive}, {'_id': False})

    # def mypage() 과 동일
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})
    nickname = user_info['nickname']
    ###

    # 위에서 저장된 정보들을 dictionary 형태로 doc에 저장
    doc = {
        'image': image["image"],
        'category': category_receive,
        'coffeeName': coffeename_receive,
        'starRating': starrating_receive,
        'review': reviewcontent_receive,
        'nickname': nickname,
        'Like': 0
    }
    
    # db reviews에 doc 정보들을 저장
    db.reviews.insert_one(doc)

    return jsonify({'msg': f'{nickname}님의 리뷰 작성이 완료되었습니다!'})


# 사용자가 좋아요 버튼을 누르면 좋아요 개수와 버튼의 모습이 변함
@app.route('/update_like', methods=['POST'])
def update_like():
    # def home() 과 동일
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload["id"]})
        ###

        # 클릭한 좋아요의 review_id를 받아옴
        review_id_receive = request.form["review_id_give"]
        # 유저에 따라 like와 unlike를 받아옴
        action_receive = request.form["action_give"]
        # 클릭한 리뷰의 id를 토대로 db reivews에서 정보를 받아옴
        now_review = db.reviews.find_one({'_id': ObjectId(review_id_receive)})
        # 클릭한 리뷰의 좋아요 수를 저장
        now_like = now_review['Like']
        
        # 로그인된 유저의 id와 좋아요 클릭한 review_id를 db에 저장
        doc = {
            "review_id": review_id_receive,
            "id": user_info["id"],
        }
        
        # like 라면 좋아요의 개수를 늘리고 doc을 db에 저장
        if action_receive == "like":
            db.likes.insert_one(doc)
            # db reviews의 id가 일치하는 리뷰의 좋아요 개수를 +1
            db.reviews.update_one({'_id': ObjectId(review_id_receive)},{'$set':{'Like':now_like+1}})
        else:
        # like 라면 좋아요의 개수를 줄이고 db likes에서 doc을 삭제
            db.likes.delete_one(doc)
            # db reviews의 id가 일치하는 리뷰의 좋아요 개수를 -1
            db.reviews.update_one({'_id': ObjectId(review_id_receive)}, {'$set': {'Like': now_like-1}})
            
        # like개수를 업데이트하기 위해 db reviews에서 id가 일치하는 리뷰를 찾아와 저장
        result_like = db.reviews.find_one({'_id': ObjectId(review_id_receive)},{'_id':False})
        # 페이지에 그리기 위해 정보들을 보내줌
        return jsonify({"result": "success", 'msg': 'updated', 'result_like': result_like})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 리뷰를 삭제
@app.route('/api/delete_review', methods=['POST'])
def delete_word():
    # 유저가 클릭한 해당 리뷰를 삭제하기 위해 리뷰의 id를 받아옴
    id_receive = request.form["id_give"]
    
    # db reviews에서 리뷰의 id와 일치하는 리뷰를 삭제 
    db.reviews.delete_one({"_id": ObjectId(id_receive)})

    return jsonify({'result': 'success', 'msg': '리뷰가 삭제되었습니다!'})


# 리뷰 카드를 클릭 후 상세 정보를 보여주기 위해 모달을 생성할 때 정보 전달
@app.route('/api/modal', methods=['POST'])
def card_modal():
    # def home() 과 동일
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})
    ###

    # 클릭한 리뷰 카드의 모달을 생성하기 위해 id를 받아옴
    id_receive = request.form["id_give"]

    # db reivews에서 받아온 id와 일치하는 일치하는 review의 정보를 받아옴
    review = db.reviews.find_one({"_id": ObjectId(id_receive)})

    # 로그인된 유저와 리뷰의 작성자가 일치할 때 삭제 가능
    delete_auth = bool(user_info['nickname'] == review['nickname'])
    print(review)

    # db에 있는 review id를 str 형을 보내주기 위해 형 변환
    review["_id"] = str(review["_id"])
    # 로그인된 유저의 id 정보로 review의 좋아요를 눌렀는지 확인하여 bool 형으로 저장
    review["heart_by_me"] = bool(db.likes.find_one({"review_id": review["_id"], "id": payload['id']}))

    return jsonify({'card': review, 'delete_auth': delete_auth})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)