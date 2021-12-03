# circuit-breaker 

Team : 
Adarsh Narasimha Murthy - 014952275 <br />
Anuhya Gankidi - 015897323 <br />
Rooppesh Sarankapani - 015253147 <br />
Sandesh Gupta - 015649036 <br />


![Architecture](https://github.com/sandeshgupta/circuit-breaker/blob/main/Circuit%20Breaker%20Flow.jpg)

## server.py

- Start server by running command `python3 server.py` in a terminal
- Test server by going to URL `localhost:8080`
- If you are able to access, it means server is up.

## proxy.py

- Start proxy by running command `python3 proxy.py` in a terminal 
- Test proxy by going to URL `localhost:1082`
- If you are able to access, it means proxy is up.

## Proxy and server connectivity

- Test proxy and server connectivity by going to URL `http://localhost:1082/hello`
- If you get `200` response, proxy and server is connected.

## Proxy and Circuit Breaker

- Go to URL `http://localhost:1082/get_response/<any_response_type>` and check the logs in terminal of proxy
  - Eg: `http://localhost:1082/get_response/200`, `http://localhost:82/get_response/404`
- If you see a log like this in proxy, `Return value <Response 18 bytes [404 NOT FOUND]>`, it means the Circuit breaker is able to access the response and it can update the Success/Failure accordingly.
