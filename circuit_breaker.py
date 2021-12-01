from enum import Enum
from datetime import datetime, timedelta
from flask import Response
from flask.json import jsonify

class CIRCUIT_BREAKER_STATES(Enum):
    OPEN = 1
    CLOSED = 2
    HALF_OPEN = 3

class CircuitBreaker(object):
    FAILURE_THRESHOLD_PERCENTAGE = 50 
    RECOVERY_TIME = 30
    FAILURE_WINDOW = 600
    EXCEPTION_TO_FAIL_FOR = Exception 

    def __init__(self, f, _failure_threshold_percentage=None,
                exception_to_fail_for=None):
        self._failure_threshold_percentage = _failure_threshold_percentage or self.FAILURE_THRESHOLD_PERCENTAGE
        self._state = CIRCUIT_BREAKER_STATES.CLOSED
        self._failure_count = 0
        self._total_count = 0
        self._exception_to_fail_for = exception_to_fail_for or self.EXCEPTION_TO_FAIL_FOR
        self._failure_window_time = timedelta(seconds=self.FAILURE_WINDOW)
        self._failure_window_start_time = datetime.utcnow()
        self._circuit_open_time = datetime.utcnow()
        self._circuit_recovery_time = self.RECOVERY_TIME
        self.f = f
        print("CB initialised")

    def __call__(self, arg):
        print("Entering", self.f.__name__)
        ret_val = self.f(arg)
        self._total_count += 1

        #is_circuit_open 
            #currTime < bufferTime+_circuit_open_time -> return 
            #currTime > bufferTime+_circuit_open_time -> HALF_OPEN

        #make request

            #success 
                #->close && return 
            
            #failure
                #if half_open -> open -> reset
                #else increment counters && check_for_open (threshold)




        #is_circuit_open 
            #currTime < bufferTime+_circuit_open_time -> return 
            #currTime > bufferTime+_circuit_open_time -> HALF_OPEN

        if(Response(ret_val).status_code == 200):
            CircuitBreaker.on_success(self)
            #->close && return (DONE)
        else:
            CircuitBreaker.on_failure(self)
            #if half_open -> open -> reset
            #else increment counters && check_for_open (DONE)
        print("Return value", ret_val)
        print("Exited", self.f.__name__)
        return ret_val

    def on_failure(self):
        self._failure_count += 1

        if (self._failure_window_start_time + self._failure_window_time) < datetime.utcnow():
            reset_counters(self)

        if (self._failure_count/self._total_count)*100 >= self._failure_threshold_percentage:
            open(self)

    def reset_counters(self):
        self._failure_count = 1
        self._total_count = 1
        self._failure_window_start_time = datetime.utcnow()

    def on_success(self):
        self._state = CIRCUIT_BREAKER_STATES.CLOSED

    def open(self):
        self._state = CIRCUIT_BREAKER_STATES.OPEN
        self._circuit_open_time = datetime.utcnow()

    def close(self):
        self._state = CIRCUIT_BREAKER_STATES.CLOSED

    def half_open(self):
        self._state = CIRCUIT_BREAKER_STATES.HALF_OPEN

    def check_state(self):
        return self._state

    def close_time(self):
        print("Not sure what to put")
        return self._circuit_open_time + timedelta(seconds = self._circuit_recovery_time)

"""
Examples to test the decorator and CB
"""
@CircuitBreaker
def server_call(path):
    print("process request on server()")

@CircuitBreaker
def server_call_2():
    print("process request on server_2()")

server_call('aa')
# server_call_2()
