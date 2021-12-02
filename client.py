import requests
import time


SERVER_URL = "http://localhost:1082"


def print_circuit_breaker_health(log):
    response = requests.get(SERVER_URL+"/checkCircuitBreakerHealth")
    data = response.json()
    print(log + ":-")
    print(data)

def move_circuit_breaker_to_open():
    requests.get(SERVER_URL+"/get_response/500")
    requests.get(SERVER_URL+"/get_response/500")
    requests.get(SERVER_URL+"/get_response/500")
    requests.get(SERVER_URL+"/get_response/500")


print("----------------------------------------------")
print("Test Case 1: Close to Close")
print_circuit_breaker_health("Start")

requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 2: Close to Open")
print_circuit_breaker_health("Start")

requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/500")
requests.get(SERVER_URL+"/get_response/500")
requests.get(SERVER_URL+"/get_response/500")
requests.get(SERVER_URL+"/get_response/500")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 3: Open to Half-Open to Open (After Time Period)")

move_circuit_breaker_to_open()
print_circuit_breaker_health("Start")

time.sleep(35)

requests.get(SERVER_URL+"/get_response/500")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 4: Open to Half-Open to Close (After Time Period)")

move_circuit_breaker_to_open()
print_circuit_breaker_health("Start")

time.sleep(35)

requests.get(SERVER_URL+"/get_response/200")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 5: Open to Open")

move_circuit_breaker_to_open()
print_circuit_breaker_health("Start")

requests.get(SERVER_URL+"/get_response/500")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 6: Close to Close with TIMEOUT")
print_circuit_breaker_health("Start")

requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 7: Close to Open when TIMEOUT")
print_circuit_breaker_health("Start")

requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 8: Open to HalfOpen to Open (After Time Period) when TIMEOUT")
print_circuit_breaker_health("Start")

time.sleep(35)

requests.get(SERVER_URL+"/timeout")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")

print("----------------------------------------------")
print("Test Case 9: Open to Half-Open to Close (After Time Period) with TIMEOUT")

move_circuit_breaker_to_open()
print_circuit_breaker_health("Start")

time.sleep(35)

requests.get(SERVER_URL+"/get_response/200")
requests.get(SERVER_URL+"/timeout")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 10: Open to Open with TIMEOUT")

move_circuit_breaker_to_open()
print_circuit_breaker_health("Start")

requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")
requests.get(SERVER_URL+"/timeout")

print_circuit_breaker_health("End")
requests.post(SERVER_URL+"/resetCircuitBreaker")

