from enum import Enum
from datetime import datetime

class CIRCUIT_BREAKER_STATES(Enum):
    OPEN = 1
    CLOSED = 2
    HALF_OPEN = 3

class CircuitBreaker(object):
    FAILURE_THRESHOLD_PERCENTAGE = 50 
    EXCEPTION_TO_FAIL_FOR = Exception 

    def __init__(self, f, _failure_threshold_percentage=None,
                exception_to_fail_for=None):
        self._failure_threshold_percentage = _failure_threshold_percentage or self.FAILURE_THRESHOLD_PERCENTAGE
        self._state = CIRCUIT_BREAKER_STATES.CLOSED
        self._failure_count = 0
        self._exception_to_fail_for = exception_to_fail_for or self.EXCEPTION_TO_FAIL_FOR
        self._failure_window_time = datetime.utcnow()
        self.f = f
        print("CB initialised")

    def __call__(self):
        print("Entering", self.f.__name__)
        self.f()
        print("Exited", self.f.__name__)

    def on_failure():
        print("Check the CB for state change. close to open?")

    def on_success():
        print("Check the CB for state change. open to close?")

    def open(self):
        self._state = CIRCUIT_BREAKER_STATES.OPEN

    def close(self):
        self._state = CIRCUIT_BREAKER_STATES.CLOSED

    def half_open(self):
        self._state = CIRCUIT_BREAKER_STATES.HALF_OPEN

    def check_state(self):
        return self._state

    def close_time():
        print("Not sure what to put")


"""
Examples to test the decorator and CB
"""
@CircuitBreaker
def server_call():
    print("process request on server()")

@CircuitBreaker
def server_call_2():
    print("process request on server_2()")

server_call()
server_call_2()
