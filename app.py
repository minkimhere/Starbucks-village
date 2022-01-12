from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, redirect, url_for
from bson import ObjectId
import requests


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.starbucksVillage


@app.route('/')
def home():
    reviews = list(db.reviews.find({}))
    for review in reviews:
        review["review_id"] = str(review["_id"])
        # review["heart_by_me"] = bool(db.likes.find_one({"review_id": review["review_id"], "id": payload['id']}))
        print(review)
    return render_template('main.html', reviews=reviews)


@app.route('/write')
def review():

    return render_template('index.html')


@app.route('/api/sort', methods=['POST'])
def review_sort():
    select_receive = request.form['select_give']
    reviews = list(db.reviews.find({'category': select_receive}, {'_id': False}))

    print(reviews)

    return render_template(review_category=reviews["category"])


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
    nickname_receive = request.form['nickname_give']

    image = db.coffees.find_one({'coffeeName': coffeename_receive}, {'_id': False})

    doc = {
        'image': image["image"],
        'category': category_receive,
        'coffeeName': coffeename_receive,
        'starRating': starrating_receive,
        'review': reviewcontent_receive,
        'nickname': nickname_receive,
        'Like': 0
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': f'{nickname_receive}님의 리뷰 작성이 완료되었습니다!'})

@app.route('/api/like_review', methods=['POST'])
def like_review():
    review_receive = request.form['review_give']

    review_target = db.reviews.find_one({'review': review_receive}, {'_id': False})
    print(review_target)
    current_like = review_target['Like']
    print(current_like)
    new_like = current_like + 1
    print(new_like)
    db.reviews.update_one({'review': review_receive}, {'$set': {'Like': new_like}})

    return jsonify()

@app.route('/api/delete_review', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    review_receive = request.form["review_give"]

    db.reviews.delete_one({"review": review_receive})

    return jsonify({'result': 'success', 'msg': '리뷰 삭제'})

@app.route('/api/modal', methods=['POST'])
def card_modal():

    id_receive = request.form["id_give"]

    review = db.reviews.find_one({"_id": ObjectId(id_receive)})
    print(review)
    review["_id"] = str(review["_id"])

    return jsonify({'card': review})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)