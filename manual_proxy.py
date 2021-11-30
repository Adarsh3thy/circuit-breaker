from flask import Flask,request,redirect,Response
import requests
from circuit_breaker import CircuitBreaker

app = Flask(__name__)

SITE_NAME = 'http://localhost:8080/'

@app.route('/')
def index():
    return 'This is proxy!'

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
        resp = requests.delete(f'{SITE_NAME}{path}').content
        response = Response(resp.content, resp.status_code)
        return response

@app.route('/<path:path>',methods=['GET','POST','DELETE'])
def proxy(path):
    return proxy_request(path)

if __name__ == '__main__':
    app.run(debug = False,port=82)