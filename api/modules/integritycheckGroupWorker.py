#!/usr/bin/env python3

# SchoolConnect Backend
# Integrity check group worker class
# © 2020 Johannes Kreutz.

# Include dependencies
import threading
import queue

# Include modules
from modules.integritycheckWorker import integritycheckWorker

# Class definition
class integritycheckGroupWorker(integritycheckWorker):
    def __init__(self, queue, lock, resultLock, results):
        integritycheckWorker.__init__(self, queue, lock, resultLock, results)
        while True:
            self.lock.acquire()
            if not self.queue.empty():
                group = self.queue.get()
                self.lock.release()
                groupResult = self.checkers.checkLdapGroupEntry(group)
                if groupResult == False:
                    self.insertToResponse(group["id"], "ERR_LDAP_ENTRY_MISSING")
                elif isinstance(groupResult, list):
                    self.insertToResponse(group["id"], "ERR_LDAP_ENTRY_INCOMPLETE", groupResult)
            else:
                self.lock.release()
                break
