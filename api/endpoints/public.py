#!/usr/bin/env python3

# SchoolConnect Backend
# Public API endpoints
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request

# Include modules
from modules.integritycheckCheckers import integritycheckCheckers
import modules.database as db
import modules.ldap as ldap
import helpers.ipfire as ipfire

# Create objects
checkers = integritycheckCheckers()

# Endpoint definition
publicApi = Blueprint("publicApi", __name__)
@publicApi.route("/api/public/usercheck/<id>", methods=["POST"])
def checkUser(id):
    dbconn = db.database()
    ldapUsers = ldap.users()
    dbconn.execute("SELECT P.id, P.firstname, P.lastname, P.preferredname, P.username, P.smb_homedir, P.email, H.smb_hash, H.unix_hash, P.unix_userid FROM people P INNER JOIN userpassword H ON H.people_id = P.id WHERE P.id = %s", (id,))
    user = dbconn.fetchone()
    check = checkers.checkLdapUserEntry(user)
    if check == False or isinstance(check, list):
        ldapResult = ldapUsers.update(id)
        if ldapResult == -1:
            return "ERR_LDAP_ERROR", 500
        if ldapResult == -2:
            return "ERR_DATABASE_ERROR", 500
    return "SUCCESS", 200

@publicApi.route("/api/public/ipfire", methods=["POST"])
def updateIpfire():
    if ipfire.updateIpfire():
        return "SUCCESS", 200
    return "ERR_UPDATE_IPFIRE", 200
