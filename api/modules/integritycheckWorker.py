#!/usr/bin/env python3

# SchoolConnect Backend
# Integrity check worker base
# © 2020 Johannes Kreutz.

# Include dependencies
import threading
import queue

# Import modules
from modules.integritycheckCheckers import integritycheckCheckers

# User worker thread class definition
class integritycheckWorker(threading.Thread):
    def __init__(self, queue, lock, resultLock, results):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.resultLock = resultLock
        self.response = results
        self.checkers = integritycheckCheckers()

    def insertToResponse(self, id, error, details = None):
        self.resultLock.acquire()
        if not id in self.response.keys():
            self.response[id] = {}
        self.response[id][error] = details
        self.resultLock.release()
