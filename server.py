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

@app.route('/get_response/<responseCode>',methods=['GET','POST','DELETE'])
def get_response(responseCode):
    logging.info('Request response {}'.format(responseCode))
    respcode=int(responseCode)
    if(respcode<300):
        resp='Success!!'
    elif(respcode>=300 and respcode<400):
        resp='You must take additional action to complete the request'
    elif(respcode>=400 and respcode<500):
        resp='Bad Request'
    else:
        resp='Internal Server error'
    return 'Response from server: '+resp, responseCode

@app.route('/timeout/',methods=['GET'])
def timeout():
    logging.info('Sleeping for {} seconds'.format(TIMEOUT_SECONDS))
    time.sleep(TIMEOUT_SECONDS)
    return 'Timeout response', 200


if __name__ == '__main__':
    app.run(debug = False,port=8080)

