# ~ encoding: utf-8  ~

import time
import random
from functools import wraps


class RateLimitBackPressure(Exception):
    pass


class MaxRetriesReached(Exception):
    pass


class RateLimit(object):
    """Ratelimit token bucket con backoff

    Se inicializa con los parámetros de bucket y retries y luego se usa como decorador de las funciones a limitar.

    Las funciones deben levantar la excepción RateLimitBackPressure para indicar que se debe incrementar el backoff.

    Si se llamó a la función demasiadas veces, se levanta la excepción MaxRetriesReached
    """

    def __init__(self,
                 bucket=20,
                 token_time=None,
                 max_retries=10,
                 wait_callback=lambda x: None,
                 empty_bucket_callback=lambda: None,
                 backoff_callback=lambda x, y: None,
                 scale_down_factor=3,
                 max_backoff=60,
                 ):

        self.scale_down_factor = scale_down_factor
        self.bucket_fill = bucket
        self.bucket_size = bucket

        if token_time is None:
            random.seed(time.clock())
            token_time = random.uniform(0.3, 0.8)
        self.token_time = token_time

        self.max_retries = max_retries
        self.max_backoff = max_backoff

        self.last_pressure = 0
        self.backoff = 0
        self.last_tick = time.time()

        self.wait_callback = wait_callback
        self.empty_bucket_callback = empty_bucket_callback
        self.backoff_callback = backoff_callback

    @property
    def under_pressure(self):
        return (time.time() - self.last_pressure) < (self.backoff * self.scale_down_factor)

    def replenish_bucket(self):
        time_delta = time.time() - self.last_tick

        token_time = max(self.token_time, self.backoff)

        for i in range(int(time_delta / token_time)):
            if self.bucket_fill < self.bucket_size:
                self.last_tick = time.time()
                self.bucket_fill += 1

    def sleep_and_notify(self, secs):
        time.sleep(secs)
        self.wait_callback(secs)

    def set_backoff(self, new_value):
        old_value = self.backoff
        if new_value > self.max_backoff:
            new_value = self.max_backoff
        self.backoff = new_value
        self.backoff_callback(new_value, old_value)

    def __call__(self, f):
        @wraps(f)
        def ratelimited_function(*args, **kwargs):
            n = 1
            while n <= self.max_retries:
                self.replenish_bucket()

                if self.bucket_fill == 0:
                    self.sleep_and_notify(self.token_time)
                    self.empty_bucket_callback()
                    continue

                if self.backoff:
                    self.sleep_and_notify(self.backoff)

                self.bucket_fill -= 1

                try:
                    n += 1
                    result = f(*args, **kwargs)

                    if not self.under_pressure:
                        self.set_backoff(max(0, self.backoff - 1))

                    return result
                except RateLimitBackPressure:
                    self.bucket_fill = 0

                    self.last_pressure = time.time()

                    if self.backoff == 0:
                        self.set_backoff(self.token_time)
                    else:
                        self.set_backoff(self.backoff * 2)
                    continue
            raise MaxRetriesReached()

        return ratelimited_function
