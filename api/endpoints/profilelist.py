#!/usr/bin/env python3

# SchoolConnect Backend
# Profile list API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db

# Endpoint definition
profileListApi = Blueprint("profileListApi", __name__)
@profileListApi.route("/api/profiles", methods=["GET"])
@login_required
def listProfiles():
    if not es.isAuthorized("devimgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    dbconn.execute("SELECT name, comment, networklockDefault, allowVNC, id FROM devprofile")
    profiles = []
    for profile in dbconn.fetchall():
        profiles.append(profile)
    return jsonify(profiles), 200
