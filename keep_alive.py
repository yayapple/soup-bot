from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return '<div style="font-family: comic Sans Ms;position: absolute; top:0; bottom: 20vh; left: 0; right: 0; margin: auto; font-size: 40px; width: 180px; height: 40px;">bot is up</div>'

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()