#!/usr/bin/env python3

# SchoolConnect Backend
# Login API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import passlib.hash

# Include modules
import modules.database as db
import modules.apiUser as apiUser
import modules.permissionCheck as pc

# Endpoint definition
loginApi = Blueprint("loginApi", __name__)
@loginApi.route("/api/login", methods=["POST"])
def createSession():
    dbconn = db.database()
    dbconn.execute("SELECT unix_hash, P.id FROM userpassword UP INNER JOIN people P ON UP.people_id = P.id WHERE P.username = %s", (request.form.get("uname"),))
    results = dbconn.fetchall()
    if not len(results) == 1:
        return "ERR_USERNAME_NOT_UNIQUE", 403
    if passlib.hash.ldap_salted_sha1.verify(request.form.get("passwd"), results[0]["unix_hash"]):
        user = apiUser.apiUser(results[0]["id"])
        login_user(user)
        pCheck = pc.permissionCheck()
        return jsonify(pCheck.get(current_user.username)), 200
    else:
        return "ERR_ACCESS_DENIED", 401

@loginApi.route("/api/logout", methods=["POST"])
def removeSession():
    logout_user()
    return "SUCCESS", 200

@loginApi.route("/api/current", methods=["GET"])
@login_required
def getCurrentUserName():
    dbconn = db.database()
    dbconn.execute("SELECT firstname FROM people WHERE username = %s", (current_user.username,))
    return jsonify({"name": dbconn.fetchone()["firstname"]}), 200
