#!/usr/bin/env python3

# SchoolConnect Backend
# Profile API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
import json
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db

# Endpoint definition
profileApi = Blueprint("profileApi", __name__)
@profileApi.route("/api/profile/<id>", methods=["GET", "PUT", "DELETE"])
@login_required
def profile(id):
    if not es.isAuthorized("devimgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    if request.method == "GET":
        dbconn.execute("SELECT name, comment, networklockDefault FROM devprofile WHERE id = %s", (id,))
        profile = dbconn.fetchone()
        profile["groups"] = []
        profile["shares"] = []
        dbconn.execute("SELECT group_id FROM devprofile_has_groups WHERE devprofile_id = %s", (id,))
        for group in dbconn.fetchall():
            profile["groups"].append(group["group_id"])
        dbconn.execute("SELECT shares_id FROM devprofile_has_shares WHERE devprofile_id = %s", (id,))
        for share in dbconn.fetchall():
            profile["shares"].append(share["shares_id"])
        return jsonify(profile), 200
    elif request.method == "PUT":
        dbconn.execute("UPDATE devprofile SET name = %s, comment = %s, networklockDefault = %s WHERE id = %s", (request.form.get("name"), request.form.get("comment"), request.form.get("networklockDefault"), id))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
    elif request.method == "DELETE":
        dbconn.execute("SELECT COUNT(*) AS count FROM device D INNER JOIN devprofile DP ON DP.id = D.devprofile_id WHERE DP.id = %s", (id,))
        count = dbconn.fetchone()["count"]
        if not count == 0:
            return "ERR_PROFILE_IN_USE", 409
        dbconn.execute("DELETE FROM devprofile WHERE id = %s", (id,))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200

@profileApi.route("/api/profile", methods=["POST"])
@login_required
def createProfile():
    if not es.isAuthorized("devimgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    dbconn.execute("INSERT INTO devprofile (name, comment, networklockDefault) VALUES (%s, %s, %s)", (request.form.get("name"), request.form.get("comment"), request.form.get("networklockDefault")))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    id = dbconn.getId()
    failed = False
    if request.form.get("groups"):
        for group in json.loads(request.form.get("groups")):
            dbconn.execute("INSERT INTO devprofile_has_groups (devprofile_id, group_id) VALUES (%s, %s)", (id, group))
            if not dbconn.commit():
                failed = True
    if request.form.get("shares"):
        for share in json.loads(request.form.get("shares")):
            dbconn.execute("INSERT INTO devprofile_has_shares (devprofile_id, shares_id) VALUES (%s, %s)", (id, share))
            if not dbconn.commit():
                failed = True
    if failed:
        return "ERR_DATABASE_ERROR", 500
    return str(id), 201

@profileApi.route("/api/profile/<id>/group/<gid>", methods=["POST", "DELETE"])
@login_required
def profileGroups(id, gid):
    if not es.isAuthorized("devimgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    if request.method == "POST":
        dbconn.execute("INSERT INTO devprofile_has_groups (devprofile_id, group_id) VALUES (%s, %s)", (id, gid))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
    elif request.method == "DELETE":
        dbconn.execute("DELETE FROM devprofile_has_groups WHERE devprofile_id = %s AND group_id = %s", (id, gid))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200

@profileApi.route("/api/profile/<id>/share/<sid>", methods=["POST", "DELETE"])
@login_required
def profileShares(id, sid):
    if not es.isAuthorized("devimgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    if request.method == "POST":
        dbconn.execute("INSERT INTO devprofile_has_shares (devprofile_id, shares_id) VALUES (%s, %s)", (id, sid))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
    elif request.method == "DELETE":
        dbconn.execute("DELETE FROM devprofile_has_shares WHERE devprofile_id = %s AND shares_id = %s", (id, sid))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
