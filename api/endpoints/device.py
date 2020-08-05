#!/usr/bin/env python3

# SchoolConnect Backend
# Device API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db

# Endpoint definition
deviceApi = Blueprint("deviceApi", __name__)
@deviceApi.route("/api/device/<id>", methods=["GET", "PUT", "DELETE"])
@login_required
def device(id):
    if not es.isAuthorized("devimgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    if request.method == "GET":
        dbconn.execute("SELECT D.id, D.name, D.comment, D.devprofile_id AS devprofile, D.registered, D.networklock, D.lastknownIPv4 as ipv4, D.lastknownIPv6 as ipv6, D.requiresLogin, HW.address, HW.type as hardwareAddressType, D.people_id, D.room, D.teacher FROM device D INNER JOIN hardwareidentifier HW on HW.device_id = D.id WHERE D.id = %s", (id,));
        device = dbconn.fetchone()
        device["logins"] = []
        dbconn.execute("SELECT info, timestamp, people_id, type, affected FROM localLoginLog WHERE device_id = %s", (id,))
        for logEntry in dbconn.fetchall():
            device["logins"].append(logEntry)
        return jsonify(device), 200
    elif request.method == "PUT":
        dbconn.execute("UPDATE device SET name = %s, comment = %s, devprofile_id = %s, networklock = %s, requiresLogin = %s, teacher = %s, room = %s WHERE id = %s", (request.form.get("name"), request.form.get("comment"), request.form.get("devprofile"), request.form.get("networklock"), request.form.get("requiresLogin"), request.form.get("teacher"), request.form.get("room"), request.form.get("id")))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
    elif request.method == "DELETE":
        dbconn.execute("DELETE FROM device WHERE id = %s", (id,))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200

@deviceApi.route("/api/device/<id>/user/<uid>", methods=["POST", "DELETE"])
@login_required
def deviceUser(id, uid):
    if not es.isAuthorized("devimgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    if request.method == "POST":
        dbconn.execute("UPDATE device SET people_id = %s WHERE id = %s", (uid, id))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
    elif request.method == "DELETE":
        dbconn.execute("UPDATE device SET people_id = NULL WHERE id = %s", (id))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200
