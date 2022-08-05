from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import random
import requests


app = Flask(__name__)


@app.route("/")
def index():
    character = requests.get(f"https://swapi.dev/api/people/{random.randint(1,80)}/")
    character = character.json()
    
    return render_template("index.html", character=character)

@app.route('/refresh')
def refresh():
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5001)