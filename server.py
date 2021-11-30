from flask import Flask,request,redirect,Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is server!'
    
@app.route('/hello')
def hello():
    return 'Hello on server!'

@app.route('/get_response/<responseType>',methods=['GET','POST','DELETE'])
def get_response(responseType):
    return 'Returning response', responseType

if __name__ == '__main__':
    app.run(debug = False,port=8080)
