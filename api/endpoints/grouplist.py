#!/usr/bin/env python3

# SchoolConnect Backend
# Group list API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db

# Endpoint definition
groupListApi = Blueprint("groupListApi", __name__)
@groupListApi.route("/api/groups", methods=["GET"])
@login_required
def listGroups():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    groups = []
    dbconn.execute("SELECT id, name, info, type FROM groups")
    for group in dbconn.fetchall():
        permissions = []
        dbconn.execute("SELECT P.name, P.id, P.info FROM permission P INNER JOIN groups_has_permission GHP ON P.id = GHP.permission_id INNER JOIN groups G ON G.id = GHP.group_id WHERE G.id = %s", (group["id"],))
        for permission in dbconn.fetchall():
            permissions.append(permission)
        group["permissions"] = permissions
        groups.append(group)
    return jsonify(groups), 200

@groupListApi.route("/api/groups/empty", methods=["GET"])
@login_required
def listEmptyGroups():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    groups = []
    dbconn.execute("SELECT id FROM groups WHERE type = 3 AND id NOT IN (SELECT group_id AS id FROM people_has_groups)")
    for group in dbconn.fetchall():
        groups.append(group["id"])
    return jsonify(groups), 200
