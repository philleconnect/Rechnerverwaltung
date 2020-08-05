#!/usr/bin/env python3

# SchoolConnect Backend
# Group API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
import json
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db
import modules.ldap as ldap

# Endpoint definition
groupApi = Blueprint("groupApi", __name__)
@groupApi.route("/api/group/<id>", methods=["GET", "DELETE"])
@login_required
def specificGroup(id):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    lg = ldap.groups()
    if request.method == "GET":
        dbconn.execute("SELECT name, info FROM groups WHERE id = %s LIMIT 1", (id,))
        group = dbconn.fetchone()
        group["permissions"] = []
        group["users"] = []
        dbconn.execute("SELECT P.id FROM permission P INNER JOIN groups_has_permission GHP ON P.id = GHP.permission_id INNER JOIN groups G ON G.id = GHP.group_id WHERE G.id = %s", (id,))
        for permission in dbconn.fetchall():
            group["permissions"].append(permission["id"])
        dbconn.execute("SELECT P.id FROM people P INNER JOIN people_has_groups PHG ON P.id = PHG.people_id INNER JOIN groups G ON G.id = PHG.group_id WHERE G.id = %s", (id,))
        for user in dbconn.fetchall():
            group["users"].append(user["id"])
        return jsonify(group), 200
    elif request.method == "DELETE":
        if not lg.delete(id) == 0:
            return "ERR_LDAP_ERROR", 500
        dbconn.execute("DELETE FROM groups WHERE id = %s", (id,))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200

@groupApi.route("/api/group", methods=["POST"])
@login_required
def createGroup():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    lg = ldap.groups()
    failed = False
    dbconn.execute("INSERT INTO groups (name, info, type) VALUES (%s, %s, %s)", (request.form.get("name"), request.form.get("info"), request.form.get("type")))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    id = dbconn.getId()
    if not lg.create(id) == 0:
        return "ERR_LDAP_ERROR", 500
    if request.form.get("permissions"):
        permissions = []
        for permission in json.loads(request.form.get("permissions")):
            permissions.append((id, permission))
        dbconn.execute("INSERT INTO groups_has_permission (group_id, permission_id) VALUES (%s, %s)", permissions)
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
    usersToAdd = []
    if request.form.get("fromgroup"):
        for group in request.form.get("source"):
            dbconn.execute("SELECT P.id FROM people P INNER JOIN people_has_groups PHG ON P.id = PHG.people_id INNER JOIN groups G ON G.id = PHG.group_id WHERE G.id = %s", (group,))
            for user in dbconn.fetchall():
                if not user in usersToAdd:
                    usersToAdd.append((id, user["id"]))
    if request.form.get("users"):
        for user in json.loads(request.form.get("users")):
            usersToAdd.append((id, user))
    for element in usersToAdd:
        element = (id, element)
    dbconn.execute("INSERT INTO people_has_groups (group_id, people_id) VALUES (%s, %s)", usersToAdd)
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    for (id, element) in usersToAdd:
        if not lg.addUser(element, id) == 0:
            failed = True
    if failed:
        return "ERR_LDAP_ERROR", 500
    return str(id), 201
