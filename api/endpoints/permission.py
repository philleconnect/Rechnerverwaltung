#!/usr/bin/env python3

# SchoolConnect Backend
# Permission API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db

# Endpoint definition
permissionApi = Blueprint("permissionApi", __name__)
@permissionApi.route("/api/permissions", methods=["GET"])
@login_required
def listPermissions():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    permissions = []
    dbconn.execute("SELECT id, name, info FROM permission")
    for permission in dbconn.fetchall():
        permissions.append(permission)
    return jsonify(permissions), 200

@permissionApi.route("/api/permission/<id>/group/<gid>", methods=["POST", "DELETE"])
@login_required
def manageGroupPermissions(id, gid):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    if request.method == "POST":
        dbconn.execute("INSERT INTO groups_has_permission (group_id, permission_id) VALUES (%s, %s)", (gid, id))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
    elif request.method == "DELETE":
        dbconn.execute("DELETE FROM groups_has_permission WHERE group_id = %s AND permission_id = %s", (gid, id))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
