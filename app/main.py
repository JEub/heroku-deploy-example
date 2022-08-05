from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import random
import requests

import os


app = Flask(__name__)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

@app.route("/")
def index():
    character = requests.get(f"https://swapi.dev/api/people/{random.randint(1,80)}/")
    character = character.json()
    
    stats = load_and_get_stats(character)

    return render_template("index.html", character=character, stats=stats)

@app.route('/refresh')
def refresh():
    return redirect('/')

@app.route('/clear')
def clear():
    mongo.db.displaystats.delete_many({})
    return redirect('/')

def load_and_get_stats(body: dict) -> dict:
    chars = mongo.db.displaystats

    chars.update_one({'name': body['name']}, {'$inc':{'displayed': 1}}, upsert=True)

    return chars.find()

if __name__ == "__main__":
    app.run(debug=True, port=5001)