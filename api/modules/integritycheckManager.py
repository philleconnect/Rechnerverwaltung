#!/usr/bin/env python3

# SchoolConnect Backend
# Integrity check manager class
# © 2020 Johannes Kreutz.

# Include dependencies
import threading
import queue
import multiprocessing
import time
import schedule

# Include modules
import modules.database as db
from modules.integritycheckUserWorker import integritycheckUserWorker
from modules.integritycheckGroupWorker import integritycheckGroupWorker

# Main class definition
class integritycheckManager:
    def __init__(self):
        self.__status = 0 # (0 -> fresh, 1 -> running, 2 -> results ready)
        self.__results = {
            "groups": {},
            "users": {}
        }
        self.__lastRun = None
        self.__workerThread = None
        self.__groupLock = threading.Lock()
        self.__groupWriteLock = threading.Lock()
        self.__groupQueue = queue.Queue()
        self.__groupThreads = []
        self.__userLock = threading.Lock()
        self.__userWriteLock = threading.Lock()
        self.__userQueue = queue.Queue()
        self.__userThreads = []
        self.run()
        schedule.every().day.at("03:00").do(self.run)

    # Run a new check
    def run(self):
        if not self.__status == 1:
            self.__status = 1
            self.__results = {
                "groups": {},
                "users": {}
            }
            self.__workerThread = threading.Thread(target = self.__asyncRun)
            self.__workerThread.start()

    # Run worker
    def __asyncRun(self):
        dbconn = db.database()
        dbconn.execute("SELECT id, name FROM groups")
        allGroups = {}
        self.__groupLock.acquire()
        for group in dbconn.fetchall():
            self.__groupQueue.put(group)
            allGroups[group["id"]] = group["name"]
        self.__groupLock.release()
        for i in range(self.__getMaxThreadCount()):
            thread = integritycheckGroupWorker(self.__groupQueue, self.__groupLock, self.__groupWriteLock, self.__results["groups"])
            thread.start()
            self.__groupThreads.append(thread)
        for thread in self.__groupThreads:
            thread.join()
        self.__groupThreads = []
        dbconn.execute("SELECT P.id, P.firstname, P.lastname, P.preferredname, P.username, P.smb_homedir, P.email, H.smb_hash, H.unix_hash, P.unix_userid FROM people P INNER JOIN userpassword H ON H.people_id = P.id")
        self.__userLock.acquire()
        for user in dbconn.fetchall():
            self.__userQueue.put(user)
        self.__userLock.release()
        failedGroups = []
        for key, value in self.__results["groups"].items():
            if not allGroups[key] in failedGroups:
                failedGroups.append(allGroups[key])
        for i in range(self.__getMaxThreadCount()):
            thread = integritycheckUserWorker(self.__userQueue, self.__userLock, self.__userWriteLock, self.__results["users"], failedGroups)
            thread.start()
            self.__userThreads.append(thread)
        for thread in self.__userThreads:
            thread.join()
        self.__userThreads = []
        self.__lastRun = time.time()
        self.__status = 2

    # Get current status
    def getStatus(self):
        return self.__status

    # Get results
    def getResults(self):
        if self.__status == 2:
            return self.__results
        else:
            return None

    # Get last run time
    def getLastRun(self):
        if self.__lastRun == None:
            return None
        return self.__lastRun

    # Remove a fixed error from the list
    def removeError(self, id, error, user = False):
        if user == True:
            key = "users"
        else:
            key = "groups"
        try:
            self.__results[key][id].pop(error, None)
            if len(self.__results[key][id].items()) <= 0:
                self.__results[key].pop(id, None)
        except KeyError:
            pass

    # Get number of threads we want to use
    def __getMaxThreadCount(self):
        available = multiprocessing.cpu_count()
        if available > 4:
            return int(available / 2)
        else:
            return 2
