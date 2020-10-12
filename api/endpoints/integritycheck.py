#!/usr/bin/env python3

# SchoolConnect Backend
# Integritycheck API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
import os
import json
import requests
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db
import modules.ldap as ldap
import modules.directory as directory
from modules.integritycheckCheckers import integritycheckCheckers

# Create integrity check manager
checkers = integritycheckCheckers()

# Endpoint definition
integritycheckApi = Blueprint("integritycheckApi", __name__)
@integritycheckApi.route("/api/integritycheck/status", methods=["GET"])
@login_required
def getIntegrityStatus():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    try:
        status = requests.get(url = "http://localhost:25252/status")
    except:
        return "ERR_CONNECTION_ERROR", 500
    try:
        lastRun = requests.get(url = "http://localhost:25252/lastRun")
    except:
        return "ERR_CONNECTION_ERROR", 500
    response = {
        "status": json.loads(status.text)["response"],
        "lastRun": json.loads(lastRun.text)["response"],
    }
    return jsonify(response), 200

@integritycheckApi.route("/api/integritycheck/results", methods=["GET"])
@login_required
def getIntegrityResults():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    try:
        response = requests.get(url = "http://localhost:25252/results")
    except:
        return "ERR_CONNECTION_ERROR", 500
    results = json.loads(response.text)["response"]
    if results == None:
        return "NO_RESULT_AVAILABLE", 200
    return jsonify(results), 200

@integritycheckApi.route("/api/integritycheck/run", methods=["POST"])
@login_required
def runIntegrityCheck():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    try:
        run = requests.put(url = "http://localhost:25252/run")
    except:
        return "ERR_CONNECTION_ERROR", 500
    return "SUCCESS", 200

@integritycheckApi.route("/api/integritycheck/fix/group/<id>", methods=["POST"])
@login_required
def fixGroup(id):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    ldapGroups = ldap.groups()
    dbconn.execute("SELECT name FROM groups WHERE id = %s", (id,))
    name = dbconn.fetchone()["name"]
    check = checkers.checkLdapGroupEntry({"name": name})
    if not check and request.form.get("missing"):
        ldapResult = ldapGroups.create(int(id))
        if ldapResult == -1:
            return "ERR_LDAP_ERROR", 500
        if ldapResult == -2:
            return "ERR_DATABASE_ERROR", 500
        dbconn.execute("SELECT P.id FROM people P INNER JOIN people_has_groups PHG ON PHG.people_id = P.ID INNER JOIN groups G ON G.id = PHG.group_id WHERE G.id = %s", (id,))
        addFailed = False
        for user in dbconn.fetchall():
            memberResult = ldapGroups.addUser(user["id"], id)
            if memberResult < 0:
                addFailed = True
        if addFailed:
            return "ERR_LDAP_ERROR", 500
    else:
        return "ERR_ALL_DONE", 200
    try:
        removeError = requests.delete(url = "http://localhost:25252/removeError/" + id + "/ERR_LDAP_ENTRY_MISSING/0")
    except:
        return "ERR_CONNECTION_ERROR", 500
    try:
        removeError = requests.delete(url = "http://localhost:25252/removeError/" + id + "/ERR_LDAP_ENTRY_INCOMPLETE/0")
    except:
        return "ERR_CONNECTION_ERROR", 500
    return "SUCCESS", 200

@integritycheckApi.route("/api/integritycheck/fix/user/<id>", methods=["POST"])
@login_required
def fixUser(id):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
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
    else:
        return "ERR_ALL_DONE", 200
    try:
        removeError = requests.delete(url = "http://localhost:25252/removeError/" + id + "/ERR_LDAP_ENTRY_MISSING/1")
    except:
        return "ERR_CONNECTION_ERROR", 500
    try:
        removeError = requests.delete(url = "http://localhost:25252/removeError/" + id + "/ERR_LDAP_ENTRY_INCOMPLETE/1")
    except:
        return "ERR_CONNECTION_ERROR", 500
    return "SUCCESS", 200

@integritycheckApi.route("/api/integritycheck/fix/folder/<id>", methods=["POST"])
@login_required
def fixFolder(id):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    dir = directory.directory()
    dbconn.execute("SELECT username, unix_userid FROM people WHERE id = %s", (id,))
    user = dbconn.fetchone()
    check = checkers.checkHomeFolder(user)
    if check == 1:
        if dir.create(user["username"], "users") < 0:
            return "ERR_CREATE_HOMEFOLDER", 500
        if not dir.setMode(user["username"], "users", "511"):
            return "ERR_FOLDER_ERROR", 500
    if check >= 1:
        if not dir.setOwner(user["username"], "users", user["unix_userid"]):
            return "ERR_FOLDER_ERROR", 500
    try:
        removeError = requests.delete(url = "http://localhost:25252/removeError/" + id + "/ERR_HOMEFOLDER_MISSING/1")
    except:
        return "ERR_CONNECTION_ERROR", 500
    try:
        removeError = requests.delete(url = "http://localhost:25252/removeError/" + id + "/ERR_HOMEFOLDER_PERMISSIONS/1")
    except:
        return "ERR_CONNECTION_ERROR", 500
    return "SUCCESS", 200

@integritycheckApi.route("/api/integritycheck/fix/membership/<id>", methods=["POST"])
@login_required
def fixGroupMembership(id):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    ldapGroups = ldap.groups()
    dbconn.execute("SELECT username FROM people WHERE id = %s", (id,))
    username = dbconn.fetchone()["username"]
    for target in json.loads(request.form.get("targets")):
        dbconn.execute("SELECT id FROM groups WHERE name = %s", (target,))
        gid = dbconn.fetchone()["id"]
        if not checkers.checkLdapGroupMembership(username, gid):
            memberResult = ldapGroups.addUser(id, gid)
            if memberResult == -1:
                return "ERR_LDAP_ERROR", 500
            if memberResult == -2:
                return "ERR_DATABASE_ERROR", 500
    try:
        removeError = requests.delete(url = "http://localhost:25252/removeError/" + id + "/ERR_LDAP_GROUP_MEMBERSHIP/1")
    except:
        return "ERR_CONNECTION_ERROR", 500
    return "SUCCESS", 200
