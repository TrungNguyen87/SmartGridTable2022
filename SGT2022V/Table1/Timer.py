# File: Timer.py
# Version 1.0
# Authors: Jop Merz
#
# Description:
# Time benchmark class
#

import time

class Timer:

    def __init__(self):
        self.__start_time   = None
        self.elapsed_time = None

    def start(self):
        self.__start_time = time.perf_counter()

    def stop(self):
        if self.__start_time is not None:
            self.elapsed_time = time.perf_counter() - self.__start_time
            self.__start_time = None
