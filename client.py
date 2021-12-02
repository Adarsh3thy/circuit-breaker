import requests
import time

SERVER_URL = "http://localhost:1082"


def print_circuit_breaker_health(log):
    response = requests.get(SERVER_URL+"/checkCircuitBreakerHealth")
    data = response.json()
    print(log + ":-")
    print(data)


print("----------------------------------------------")
print("Test Case 1: Close to Close")
print_circuit_breaker_health("Start")

response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")

print_circuit_breaker_health("End")
response = requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 2: Close to Open")
print_circuit_breaker_health("Start")

response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/200")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")

print_circuit_breaker_health("End")
response = requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 3: Open to Half-Open to Open (After Time Period)")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")

print_circuit_breaker_health("Start")

time.sleep(35)

response = requests.get(SERVER_URL+"/get_response/500")

print_circuit_breaker_health("End")
response = requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 4: Open to Half-Open to Close (After Time Period)")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")

print_circuit_breaker_health("Start")

time.sleep(35)

response = requests.get(SERVER_URL+"/get_response/200")

response = requests.get(SERVER_URL+"/checkCircuitBreakerHealth")
data = response.json()
print("End: ")
print(data)
response = requests.post(SERVER_URL+"/resetCircuitBreaker")


print("----------------------------------------------")
print("Test Case 5: Open to Open")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")
response = requests.get(SERVER_URL+"/get_response/500")

print_circuit_breaker_health("Start")

response = requests.get(SERVER_URL+"/get_response/500")

response = requests.get(SERVER_URL+"/checkCircuitBreakerHealth")
data = response.json()
print("End: ")
print(data)
response = requests.post(SERVER_URL+"/resetCircuitBreaker")
