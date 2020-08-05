#!/usr/bin/env python3

# SchoolConnect Backend
# User list API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db

# Endpoint definition
userListApi = Blueprint("userListApi", __name__)
@userListApi.route("/api/users", methods=["GET"])
@login_required
def listUsers():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    users = []
    dbconn.execute("SELECT id, firstname, lastname, username, email, DATE_FORMAT(birthdate, '%Y-%m-%d') AS birthdate, persistant FROM people")
    for user in dbconn.fetchall():
        ids = []
        dbconn.execute("SELECT G.id AS id FROM groups G INNER JOIN people_has_groups PHG ON PHG.group_id = G.id INNER JOIN people P ON P.id = PHG.people_id WHERE P.id = %s", (user["id"],))
        for group in dbconn.fetchall():
            ids.append(group["id"])
        user["groups"] = ids
        users.append(user)
    return jsonify(users), 200
