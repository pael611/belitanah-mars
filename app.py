from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/mars", methods=["POST"])
def movie_post():
    try:
        name_receive = request.form['name_give']
        address_receive = request.form['address_give']
        size_receive = request.form['size_give']
        doc = {
            'name':name_receive,
            'address':address_receive,
            'size':size_receive
        }

        db.mars.insert_one(doc)
        return jsonify({'msg':'POST request!'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/show/mars", methods=["GET"])
def show_order():
    movie_list = list(db.mars.find({},{'_id':False}))
    return jsonify({'buyers':movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)