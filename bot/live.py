from flask import Flask
from threading import Thread


app = Flask('')



@app.route('/')
def home():
    return 'i am alive =)'

def run():
    app.run('0.0.0.0',port=8080)

def alive():
    t = Thread(target=run)
    t.start()

