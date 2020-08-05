#!/usr/bin/env python3

# SchoolConnect Backend
# Share group API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db
import helpers.samba as samba

# Endpoint definition
shareGroupApi = Blueprint("shareGroupApi", __name__)
@shareGroupApi.route("/api/share/<id>/group/<gid>", methods=["POST", "DELETE", "PUT"])
@login_required
def listShares(id, gid):
    if not es.isAuthorized(["usermgmt","devimgmt"]):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    if request.method == "POST":
        permissions = 1
        if request.form.get("permissions"):
            permissions = int(request.form.get("permissions"))
        dbconn.execute("INSERT INTO groups_has_shares (shares_id, group_id, permission) VALUES (%s, %s, %s)", (id, gid, permissions))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        if not samba.update():
            return "ERR_UPDATE_SAMBA", 500
        return "SUCCESS", 201
    elif request.method == "PUT":
        dbconn.execute("UPDATE groups_has_shares SET permission = %s WHERE shares_id = %s AND group_id = %s", (request.form.get("permission"), id, gid))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        if not samba.update():
            return "ERR_UPDATE_SAMBA", 500
        return "SUCCESS", 200
    elif request.method == "DELETE":
        dbconn.execute("DELETE FROM groups_has_shares WHERE shares_id = %s AND group_id = %s", (id, gid))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        if not samba.update():
            return "ERR_UPDATE_SAMBA", 500
        return "SUCCESS", 200
