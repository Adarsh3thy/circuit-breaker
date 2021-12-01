from flask import Flask,request,redirect,Response
import time
import logging

logging.basicConfig(level=logging.INFO)

TIMEOUT_SECONDS = 5

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is server!'
    
@app.route('/hello')
def hello():
    return 'Hello on server!'

@app.route('/get_response/<responseType>',methods=['GET','POST','DELETE'])
def get_response(responseType):
    logging.info('Request response {}'.format(responseType))
    return 'Returning response', responseType

@app.route('/timeout/<timeout_seconds>',methods=['GET'])
def timeout(timeout_seconds):
    logging.info('Sleeping for {} seconds'.format(timeout_seconds))
    time.sleep(TIMEOUT_SECONDS)
    return 'Timeout response', 200

@app.route('/failure',methods=['GET'])
def faulty_endpoint():
    return Response("{'msg': 'I always fail.'}", status=500)

if __name__ == '__main__':
    app.run(debug = False,port=8080)
