from enum import Enum
from datetime import datetime, timedelta
from flask import Response
from flask.json import jsonify
import logging
import redis
import sys

logging.basicConfig(level=logging.INFO)

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

class CIRCUIT_BREAKER_STATES(Enum):
    OPEN = 1
    CLOSED = 2
    HALF_OPEN = 3

class CircuitBreaker(object):
    FAILURE_COUNT_THRESHOLD = 3
    RECOVERY_TIME = 30
    FAILURE_WINDOW = 600
    EXCEPTION_TO_FAIL_FOR = Exception 

    def __init__(self, f, _failure_count_threshold=None,
                 exception_to_fail_for=None):
        self._failure_count_threshold = _failure_count_threshold or self.FAILURE_COUNT_THRESHOLD
        self._state = CIRCUIT_BREAKER_STATES.CLOSED
        self._failure_count = 0
        self._exception_to_fail_for = exception_to_fail_for or self.EXCEPTION_TO_FAIL_FOR
        self._failure_window_time = timedelta(seconds=self.FAILURE_WINDOW)
        self._failure_window_start_time = datetime.utcnow()
        self._circuit_open_time = datetime.utcnow()
        self._circuit_recovery_time = self.RECOVERY_TIME
        self.f = f
        self.push_circuit_breaker_to_redis()
        print("CB initialised")

    def __call__(self, arg):
        print("Entering ", self.f.__name__)
        logging.info('Entering Circuit breaker')

        print("Current State of CB {}",self.check_state())
        if(self.check_state()==CIRCUIT_BREAKER_STATES.OPEN):
            current_timelapse=datetime.utcnow() - self._circuit_open_time
            print("Open state, time elapsed: {}",current_timelapse)
            if(current_timelapse.total_seconds()<CircuitBreaker.RECOVERY_TIME):
                ret_val=Response("The server is currently unavailable, please try after sometime",503)
            else:
                self.half_open()
                ret_val = self.f(arg)
                if(ret_val):
                    print("Response status: ", ret_val.status_code)
                if (ret_val and int(ret_val.status_code) < 300):
                    self.close()
                else:
                    self.open()
        else:
            ret_val = self.f(arg)
            if(ret_val):
                print("Response status: ", ret_val.status_code)
            if (ret_val and int(ret_val.status_code) < 300):
                CircuitBreaker.on_success(self)
            else:
                print("failure")
                CircuitBreaker.on_failure(self)

        self.push_circuit_breaker_to_redis()
        
        print("Exited", self.f.__name__)
        return ret_val


    def push_circuit_breaker_to_redis(self):
        redis.set('_state', int(self._state._value_))
        redis.set('_failure_count', self._failure_count)
        redis.set('_failure_window_time', str(self._failure_window_time))
        redis.set('_failure_window_start_time', self._failure_window_start_time.strftime('%B %d %Y - %H:%M:%S'))
        redis.set('_circuit_open_time', self._circuit_open_time.strftime('%B %d %Y - %H:%M:%S'))
        redis.set('_circuit_recovery_time', self._circuit_recovery_time)

    def on_failure(self):
        self._failure_count += 1

        if (self._failure_window_start_time + self._failure_window_time) < datetime.utcnow():
            self.reset_counters()

        print(self._failure_count)

        if self._failure_count >= self._failure_count_threshold:
            self.open()

    def reset_counters(self):
        print("Counters reset")
        self._failure_count = 0
        self._failure_window_start_time = datetime.utcnow()

    def on_success(self):
        self._state = CIRCUIT_BREAKER_STATES.CLOSED

    def open(self):
        self._state = CIRCUIT_BREAKER_STATES.OPEN
        self._circuit_open_time = datetime.utcnow()
        self.reset_counters()

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
