#!/usr/bin/env python3

# SchoolConnect Backend
# LDAP connector
# © 2020 Johannes Kreutz.

# Include dependencies
import time
from ldap3 import Server, Connection, ALL, Writer, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE
from ldap3.utils.conv import escape_filter_chars

# Include modules
import modules.configfile as cf
import modules.database as db

# Base class definition
class ldap:
    def __init__(self):
        self.config = cf.configfile()
        ldapServer = Server(self.config.get("ldap", "url"))
        self.connection = Connection(ldapServer, self.config.get("ldap", "admindn") + "," + self.config.get("ldap", "basedn"), self.config.get("ldap", "password"), auto_bind=True)

    # Helper to get user or group name
    def getName(self, id, user = False):
        query = "SELECT username AS name FROM people WHERE id = %s LIMIT 1" if user else "SELECT name FROM groups WHERE id = %s LIMIT 1"
        dbconn = db.database()
        try:
            dbconn.execute(query, (id,))
            result = dbconn.fetchone()
            return result["name"]
        except:
            return False

# Ldap group manager
class groups(ldap):
    def __init__(self):
        ldap.__init__(self)

    # Create a new ldap group
    def create(self, id):
        group = self.getName(id)
        if group == False:
            return -2
        self.connection.search(self.config.get("ldap", "basedn"), "(sambaDomainName=" + self.config.get("ldap", "sambahostname") + ")", attributes=["sambaSID"])
        sambaSID = self.connection.entries[0]["sambaSID"]
        groupId = id + 10000
        groupEntry = {
            "cn": group,
            "displayName": group,
            "gidNumber": groupId,
            "objectClass": ["top", "posixGroup", "sambaGroupMapping"],
            "sambaGroupType": "2",
            "sambaSID": str(sambaSID) + "-" + str(groupId),
        }
        try:
            self.connection.add("cn=" + group + "," + self.config.get("ldap", "groupsdn") + "," + self.config.get("ldap", "basedn"), "posixGroup", groupEntry)
        except:
            return -1
        else:
            return 0

    # Delete a group from ldap
    def delete(self, id):
        group = self.getName(id)
        if group == False:
            return -2
        try:
            self.connection.delete("cn=" + group + "," + self.config.get("ldap", "groupsdn") + "," + self.config.get("ldap", "basedn"))
        except:
            return -1
        else:
            return 0

    # Add a user to a ldap group
    def addUser(self, userid, id):
        group = self.getName(id)
        if group == False:
            return -2
        user = self.getName(userid, True)
        if user == False:
            return -2
        try:
            self.connection.modify("cn=" + group + "," + self.config.get("ldap", "groupsdn") + "," + self.config.get("ldap", "basedn"), {
                "memberUid": [(MODIFY_ADD, [user])]
            })
        except:
            return -1
        else:
            return 0

    # Remove a user from a ldap group
    def deleteUser(self, userid, id):
        group = self.getName(id)
        if group == False:
            return -2
        user = self.getName(userid, True)
        if user == False:
            return -2
        try:
            self.connection.modify("cn=" + group + "," + self.config.get("ldap", "groupsdn") + "," + self.config.get("ldap", "basedn"), {
                "memberUid": [(MODIFY_DELETE, [user])]
            })
        except:
            return -1
        else:
            return 0

    # List all ldap groups
    def list(self, cn = "*"):
        cn = escape_filter_chars(cn)
        self.connection.search(self.config.get("ldap", "groupsdn") + "," + self.config.get("ldap", "basedn"), "(cn=" + cn + ")", attributes=["cn"])
        groups = []
        for entry in self.connection.entries:
            groups.append({
                "name": entry["cn"][0],
            })
        return groups

    # List all users of a ldap group
    def listUsers(self, id):
        users = []
        group = self.getName(id)
        if group == False:
            return -2
        group = escape_filter_chars(group)
        try:
            self.connection.search(self.config.get("ldap", "groupsdn") + "," + self.config.get("ldap", "basedn"), "(cn=" + group + ")", attributes=["memberUid"])
            users = self.connection.entries[0]["memberUid"]
        except:
            return -1
        else:
            if len(users) == 0:
                return []
            return users

# Ldap user manager
class users(ldap):
    def __init__(self):
        ldap.__init__(self)

    # List all users
    def list(self, uid = "*"):
        self.connection.search(self.config.get("ldap", "usersdn") + "," + self.config.get("ldap", "basedn"), "(uid=" + uid + ")", attributes=["uid", "displayName", "homeDirectory", "mail", "sn", "sambaNTPassword", "userPassword", "uidNumber"])
        users = []
        for entry in self.connection.entries:
            users.append({
                "username": entry["uid"][0],
                "preferredname": entry["displayName"][0],
                "smb_homedir": entry["homeDirectory"][0],
                "email": entry["mail"][0],
                "lastname": entry["sn"][0],
                "smb_hash": entry["sambaNTPassword"][0],
                "unix_hash": entry["userPassword"][0],
                "unix_userid": entry["uidNumber"][0],
            })
        return users

    # Create or update a user
    def update(self, id):
        dbconn = db.database()
        try:
            dbconn.execute("SELECT P.username, P.preferredname, P.smb_homedir, P.email, P.unix_userid, P.lastname, H.smb_hash, H.unix_hash FROM people P INNER JOIN userpassword H ON H.people_id = P.id WHERE id = %s LIMIT 1", (id,))
            result = dbconn.fetchone()
            user = {
                "cn": result["username"],
                "displayName": result["preferredname"],
                "givenName": result["preferredname"],
                "homeDirectory": result["smb_homedir"],
                "mail": result["email"],
                "userPassword": result["unix_hash"],
                "sambaHomePath": "\\\\\\" + result["username"],
                "sambaNTPassword": result["smb_hash"],
                "sambaProfilePath": "\\\\\\profiles\\" + result["username"],
                "sambaPwdLastSet": int(time.time()),
                "shadowLastChange": int(time.time()),
                "sn": result["lastname"],
                "uidNumber": result["unix_userid"],
                "uid": result["username"],
            }
            exists = False
            self.connection.search(self.config.get("ldap", "usersdn") + "," + self.config.get("ldap", "basedn"), "(uid=*)", attributes=["sn", "businessCategory", "givenName"])
            for entry in self.connection.entries:
                if entry["sn"] == result["lastname"] and entry["givenName"] == result["preferredname"] and entry["businessCategory"] == id:
                    exists = True
                    break;
            if exists:
                attributes = {}
                for key, value in user.items():
                    attributes[key] = [(MODIFY_REPLACE, [value])]
                try:
                    self.connection.modify("uid=" + result["username"] + "," + self.config.get("ldap", "usersdn") + "," + self.config.get("ldap", "basedn"), attributes)
                except:
                    return -1
                else:
                    return 0
            else:
                self.connection.search(self.config.get("ldap", "basedn"), "(sambaDomainName=" + self.config.get("ldap", "sambahostname") + ")", attributes=["sambaSID"])
                sambaSID = self.connection.entries[0]["sambaSID"]
                user["businessCategory"] = id
                user["gecos"] = "System User"
                user["gidNumber"] = "513"
                user["loginShell"] = "/bin/bash"
                user["objectClass"] = ["top", "person", "organizationalPerson", "posixAccount", "shadowAccount", "inetOrgPerson", "sambaSamAccount"]
                user["sambaAcctFlags"] = "[U]"
                user["sambaKickoffTime"] = "2147483647"
                user["sambaLogoffTime"] = "2147483647"
                user["sambaLogonTime"] = "0"
                user["sambaPrimaryGroupSID"] = str(sambaSID) + "-513"
                user["sambaPwdCanChange"] = "0"
                user["sambaPwdMustChange"] = "86401501080402"
                user["sambaSID"] = str(sambaSID) + "-" + str(result["unix_userid"])
                user["shadowMax"] = "999999999"
                try:
                    self.connection.add("uid=" + result["username"] + "," + self.config.get("ldap", "usersdn") + "," + self.config.get("ldap", "basedn"), "posixAccount", user)
                except:
                    return -1
                else:
                    return 0
        except:
            return -2

    # Remove a user from ldap
    def delete(self, id):
        user = self.getName(id, True)
        if user == False:
            return -2
        try:
            self.connection.delete("uid=" + user + "," + self.config.get("ldap", "usersdn") + "," + self.config.get("ldap", "basedn"))
        except:
            return -1
        else:
            return 0
