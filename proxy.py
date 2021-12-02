from flask import Flask,request,redirect,Response
from flask import json
from flask.json import jsonify
import requests
from circuit_breaker import CircuitBreaker
import redis
app = Flask(__name__)

SITE_NAME = 'http://localhost:8080/'

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

@app.route('/')
def index():
    return 'This is proxy!'

@app.route('/checkCircuitBreakerHealth')
def check_circuit_breaker_health():
    return json.dumps({
        "_state":str(redis.get('_state')),
        "_failure_count":str(redis.get('_failure_count')),
        "_total_count":str(redis.get('_total_count')),
        "_failure_window_time":str(redis.get('_failure_window_time')),
        "_failure_window_start_time":str(redis.get('_failure_window_start_time')),
        "_circuit_open_time":str(redis.get('_circuit_open_time')),
        "_circuit_recovery_time":str(redis.get('_circuit_recovery_time'))
    })

@app.route('/resetCircuitBreaker')
def reset_circuit_breaker():
    CircuitBreaker("reset")
    return json.dumps({"status": "Success"})

def reset():
    return 

@CircuitBreaker
def proxy_request(path):
    print("process request on server()")
    global SITE_NAME

    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='POST':
        resp = requests.post(f'{SITE_NAME}{path}',json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='DELETE':
        resp = requests.delete(f'{SITE_NAME}{path}')
        response = Response(resp.content, resp.status_code)
        return response

@app.route('/<path:path>',methods=['GET','POST','DELETE'])
def proxy(path):
    return proxy_request(path)

if __name__ == '__main__':
    app.run(debug = False,port=1082)