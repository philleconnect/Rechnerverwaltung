#!/usr/bin/env python3

# SchoolConnect Backend
# Share API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
import os
import json
from flask import Blueprint, request, jsonify
from flask_login import login_required

# Include modules
import helpers.essentials as es
import modules.database as db
import helpers.samba as samba
import modules.directory as directory

# Endpoint definition
shareApi = Blueprint("shareApi", __name__)
@shareApi.route("/api/share/<id>", methods=["DELETE"])
@login_required
def deleteShare(id):
    if not es.isAuthorized(["usermgmt","devimgmt"]):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    dbconn.execute("SELECT path FROM shares WHERE id = %s", (id,))
    result = dbconn.fetchone()
    cleanPath = result["path"][13:] if result["path"][0:13] == "/home/shares/" else result["path"]
    dbconn.execute("SELECT COUNT(*) AS num FROM shares WHERE id != %s AND path LIKE %s", (id, cleanPath,))
    count = dbconn.fetchone()["num"]
    if not count == 0:
        return "ERR_SHARE_HAS_SUBSHARE", 500
    dbconn.execute("DELETE FROM shares WHERE id = %s", (id,))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    if not samba.update():
        return "ERR_UPDATE_SAMBA", 500
    if result["path"].count("/") <= 3:
        dir = directory.directory()
        if dir.exists(cleanPath, "deleted"):
            if not dir.delete(cleanPath, "deleted") == 0:
                return "ERR_DELETE_PREVIOUS_FOLDER", 500
        if not dir.move(cleanPath, "shares", cleanPath, "deleted") == 0:
            return "ERR_FOLDER_ERROR", 500
    return "SUCCESS", 200

@shareApi.route("/api/share", methods=["POST"])
@login_required
def createShare():
    if not es.isAuthorized(["usermgmt","devimgmt"]):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    dbconn.execute("INSERT INTO shares (name, path) VALUES (%s, %s)", (request.form.get("name"), request.form.get("path")))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    failed = False
    id = dbconn.getId()
    for group in json.loads(request.form.get("group")):
        dbconn.execute("INSERT INTO groups_has_shares (shares_id, group_id, permission) VALUES (%s, %s, %s)", (id, group["id"], group["permission"]))
        if not dbconn.commit():
            failed = True
    if failed:
        return "ERR_DATABASE_ERROR", 500
    dir = directory.directory()
    if not request.form.get("isSubshare") == "true":
        cleanPath = request.form.get("path")[13:] if request.form.get("path")[0:13] == "/home/shares/" else request.form.get("path")
        if not dir.create(cleanPath, "shares") == 0:
            return "ERR_CREATE_SHAREFOLDER", 500
        if not dir.setOwner(cleanPath, "shares", 0) or not dir.setMode(cleanPath, "shares", "511"):
            return "ERR_FOLDER_ERROR", 500
    if not samba.update():
        return "ERR_UPDATE_SAMBA", 500
    return "SUCCESS", 200


@shareApi.route("/api/shares/subdirs", methods=["GET"])
@login_required
def listSubdirs():
    if not es.isAuthorized(["usermgmt","devimgmt"]):
        return "ERR_ACCESS_DENIED", 403
    basedirs = []
    for element in os.listdir("/home/shares"):
        if os.path.isdir("/home/shares/" + element):
            subdirs = []
            for subelement in os.listdir("/home/shares/" + element):
                if os.path.isdir("/home/shares/" + element + "/" + subelement):
                    subdirs.append(subelement)
            basedirs.append({
                "base": element,
                "sub": subdirs
            })
    return jsonify(basedirs), 200
