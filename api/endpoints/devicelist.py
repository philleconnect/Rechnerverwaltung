#!/usr/bin/env python3

# SchoolConnect Backend
# Device list API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db

# Endpoint definition
deviceListApi = Blueprint("deviceListApi", __name__)
@deviceListApi.route("/api/devices", methods=["GET"])
@login_required
def listDevices():
    if not es.isAuthorized("devimgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    dbconn.execute("SELECT name, comment, devprofile_id AS devprofile, people_id, networklock, screenlock, requiresLogin, id, room, teacher FROM device")
    devices = []
    for device in dbconn.fetchall():
        devices.append(device)
    return jsonify(devices), 200
