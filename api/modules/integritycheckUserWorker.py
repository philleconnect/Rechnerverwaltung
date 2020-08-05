#!/usr/bin/env python3

# SchoolConnect Backend
# Integrity check user worker class
# © 2020 Johannes Kreutz.

# Include dependencies
import threading
import queue

# Include modules
import modules.database as db
from modules.integritycheckWorker import integritycheckWorker

# Class definition
class integritycheckUserWorker(integritycheckWorker):
    def __init__(self, queue, lock, resultLock, results, failedGroups):
        integritycheckWorker.__init__(self, queue, lock, resultLock, results)
        self.__dbconn = db.database()
        self.__failedGroups = failedGroups
        while True:
            self.lock.acquire()
            if not self.queue.empty():
                user = self.queue.get()
                self.lock.release()
                userResult = self.checkers.checkLdapUserEntry(user)
                # Check users LDAP entry
                if userResult == False:
                    self.insertToResponse(user["id"], "ERR_LDAP_ENTRY_MISSING")
                elif isinstance(userResult, list):
                    self.insertToResponse(user["id"], "ERR_LDAP_ENTRY_INCOMPLETE", userResult)
                # Check user folder existance and permissions
                folderResult = self.checkers.checkHomeFolder(user)
                if folderResult == 1:
                    self.insertToResponse(user["id"], "ERR_HOMEFOLDER_MISSING")
                elif folderResult == 2:
                    self.insertToResponse(user["id"], "ERR_HOMEFOLDER_PERMISSIONS")
                # Check group memberships
                self.__dbconn.execute("SELECT G.id, G.name FROM groups G INNER JOIN people_has_groups PHG ON PHG.group_id = G.id INNER JOIN people P ON PHG.people_id = P.id WHERE P.id = %s", (user["id"],))
                missingGroupMemberships = []
                for group in self.__dbconn.fetchall():
                    if not group["name"] in self.__failedGroups and not self.checkers.checkLdapGroupMembership(user["username"], group["id"]):
                        missingGroupMemberships.append(group["name"])
                if len(missingGroupMemberships) > 0:
                    self.insertToResponse(user["id"], "ERR_LDAP_GROUP_MEMBERSHIP", missingGroupMemberships)
            else:
                self.lock.release()
                break
