#!/usr/bin/env python3

# SchoolConnect Backend
# Integritycheck checking functions class
# © 2020 Johannes Kreutz.

# Include modules
import modules.ldap as ldap
import modules.directory as directory

# Class definition
class integritycheckCheckers:
    def __init__(self):
        self.__ldapUsers = ldap.users()
        self.__ldapGroups = ldap.groups()
        self.__dir = directory.directory()

    def checkLdapGroupEntry(self, group):
        ldapGroup = self.__ldapGroups.list(group["name"]);
        if not len(ldapGroup) == 1:
            return False
        wrongParameters = []
        for key, value in ldapGroup[0].items():
            if not value == group[key]:
                wrongParameters.append(key)
        if len(wrongParameters) > 0:
            return wrongParameters
        return True

    def checkLdapUserEntry(self, user, ldapUser = None):
        if ldapUser == None:
            ldapUser = self.__ldapUsers.list(user["username"])
        if not len(ldapUser) == 1:
            return False
        wrongParameters = []
        for key, value in ldapUser[0].items():
            if isinstance(value, bytes):
                value = value.decode("utf8")
            if not value == user[key]:
                wrongParameters.append(key)
        if len(wrongParameters) > 0:
            return wrongParameters
        return True

    def checkHomeFolder(self, user):
        if not self.__dir.exists(user["username"], "users"):
            return 1
        if not self.__dir.getOwner(user["username"], "users") == user["unix_userid"]:
            return 2
        return 0

    def checkLdapGroupMembership(self, username, group):
        ldapGroupUsers = self.__ldapGroups.listUsers(group)
        for member in ldapGroupUsers:
            if member == username:
                return True
        return False

    def checkUserHasEvilTwin(self, user):
        ldapUsers = self.__ldapUsers.list()
        for ldapUser in ldapUsers:
            if not ldapUser["username"] == user["username"] and self.checkLdapUserEntry(user, ldapUser):
                return True
        return False
