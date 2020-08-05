#!/usr/bin/env python3

# SchoolConnect Backend
# Group list API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db
import modules.ldap as ldap

# Endpoint definition
userGroupApi = Blueprint("userGroupApi", __name__)
@userGroupApi.route("/api/group/<id>/user/<uid>", methods=["POST", "DELETE"])
@login_required
def groupOperation(id, uid):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    lg = ldap.groups()
    if request.method == "POST":
        dbconn.execute("INSERT INTO people_has_groups (people_id, group_id) VALUES (%s, %s)", (uid, id))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        if not lg.addUser(uid, id) == 0:
            return "ERR_LDAP_ERROR", 500
        return "SUCCESS", 201
    elif request.method == "DELETE":
        dbconn.execute("DELETE FROM people_has_groups WHERE people_id = %s AND group_id = %s", (uid, id))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        if not lg.deleteUser(uid, id) == 0:
            return "ERR_LDAP_ERROR", 500
        return "SUCCESS", 200
