from flask import Flask,request,redirect,Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is server!'
    
@app.route('/hello')
def hello():
    return 'Hello on server!'

if __name__ == '__main__':
    app.run(debug = False,port=8080)
