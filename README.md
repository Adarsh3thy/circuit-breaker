# circuit-breaker

## server.py

- Start server by running command `python3 server.py` in a terminal
- Test server by going to URL `localhost:8080`
- If you are able to access, it means server is up.

## maunal_proxy.py

- Start proxy by running command `python3 manual_proxy.py` in a terminal 
- Test proxy by going to URL `localhost:82`
- If you are able to access, it means proxy is up.

## Proxy and server connectivity

- Test proxy and server connectivity by going to URL `http://localhost:82/hello`
- If you get `200` response, proxy and server is connected.

## Proxy and Circuit Breaker

- Go to URL `http://localhost:82/get_response/<any_response_type>` and check the logs in terminal of proxy
  - Eg: `http://localhost:82/get_response/200`, `http://localhost:82/get_response/404`
- If you see a log like this in proxy, `Return value <Response 18 bytes [404 NOT FOUND]>`, it means the Circuit breaker is able to access the response and it can update the Success/Failure accordingly.
