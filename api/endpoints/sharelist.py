#!/usr/bin/env python3

# SchoolConnect Backend
# Share list API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db

# Endpoint definition
shareListApi = Blueprint("shareListApi", __name__)
@shareListApi.route("/api/shares", methods=["GET"])
@login_required
def listShares():
    if not es.isAuthorized(["usermgmt","devimgmt"]):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    dbconn.execute("SELECT name, path, id FROM shares")
    shares = []
    for share in dbconn.fetchall():
        groups = []
        dbconn.execute("SELECT G.id, G.name, GHS.permission FROM groups G INNER JOIN groups_has_shares GHS ON GHS.group_id = G.id WHERE GHS.shares_id = %s", (share["id"],))
        for group in dbconn.fetchall():
            groups.append(group)
        share["groups"] = groups
        shares.append(share)
    return jsonify(shares), 200
