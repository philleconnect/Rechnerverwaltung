#!/usr/bin/env python3

# SchoolConnect Backend
# User API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
import json
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import passlib.hash

# Include modules
import helpers.essentials as es
import modules.database as db
import modules.ldap as ldap
import modules.directory as directory
import helpers.hash as hash
import helpers.idservice as idsrv

# Endpoint definition
userApi = Blueprint("userApi", __name__)
@userApi.route("/api/user/<id>", methods=["GET", "PUT", "DELETE"])
@login_required
def specificUser(id):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    lu = ldap.users()
    lg = ldap.groups()
    dir = directory.directory()
    if request.method == "GET":
        dbconn.execute("SELECT firstname, lastname, preferredname, sex, title, short, email, DATE_FORMAT(birthdate, '%Y-%m-%d') AS birthdate, username, smb_homedir, persistant FROM people WHERE id = %s", (id,))
        user = dbconn.fetchone()
        user["groups"] = []
        user["devices"] = []
        user["logins"] = []
        dbconn.execute("SELECT G.name AS name, G.id AS id FROM groups G INNER JOIN people_has_groups PHG ON PHG.group_id = G.id INNER JOIN people P ON P.id = PHG.people_id WHERE P.id = %s", (id,))
        for group in dbconn.fetchall():
            user["groups"].append(group)
        dbconn.execute("SELECT name, id FROM device WHERE people_id = %s", (id,))
        for device in dbconn.fetchall():
            user["devices"].append(device)
        dbconn.execute("SELECT timestamp, info, D.name, D.id FROM localLoginLog LLL INNER JOIN device D ON D.id = LLL.device_id WHERE LLL.people_id = %s", (id,))
        for loginEvent in dbconn.fetchall():
            user["logins"].append(loginEvent)
        dbconn.execute("SELECT autogen, cleartext FROM userpassword WHERE people_id = %s", (id,))
        autogenPassword = dbconn.fetchone()
        if autogenPassword["autogen"] == 1:
            user["autogenPassword"] = autogenPassword["cleartext"]
        return jsonify(user), 200
    elif request.method == "PUT":
        dbconn.execute("UPDATE people SET firstname = %s, lastname = %s, email = %s, title = %s, short = %s, birthdate = %s, sex = %s, persistant = %s WHERE id = %s", (request.form.get("firstname"), request.form.get("lastname"), request.form.get("email"), request.form.get("title"), request.form.get("short"), request.form.get("birthdate"), request.form.get("sex"), request.form.get("persistant"), id))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        if not lu.update(id) == 0:
            return "ERR_LDAP_ERROR", 500
        return "SUCCESS", 200
    elif request.method == "DELETE":
        dbconn.execute("SELECT username FROM people WHERE id = %s", (id,))
        user = dbconn.fetchone()["username"]
        if user == current_user.username:
            return "ERR_ACTUAL_ACCOUNT", 400
        if not lu.delete(id) == 0:
            return "ERR_LDAP_ERROR", 500
        failed = False
        dbconn.execute("SELECT G.id FROM people P INNER JOIN people_has_groups PHG ON PHG.people_id = P.id INNER JOIN groups G ON G.id = PHG.group_id WHERE P.id = %s", (id,))
        for group in dbconn.fetchall():
            if not lg.deleteUser(id, group["id"]) == 0:
                failed = True
        if failed:
            return "ERR_LDAP_ERROR", 500
        if dir.exists(user, "deleted"):
            if not dir.delete(user, "deleted") == 0:
                return "ERR_DELETE_PREVIOUS_FOLDER", 500
        dircode = dir.move(user, "users", user, "deleted")
        if not dircode == 0 and not dircode == -2:
            return "ERR_MOVE_DATA_FOLDER", 500
        dbconn.execute("DELETE FROM people WHERE id = %s", (id,))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        return "SUCCESS", 200

@userApi.route("/api/user", methods=["POST"])
@login_required
def createUser():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dir = directory.directory()
    if dir.exists(request.form.get("username"), "users"):
        return "ERR_FOLDER_EXISTS", 500
    dbconn = db.database()
    lu = ldap.users()
    lg = ldap.groups()
    id = idsrv.getNew()
    if not request.form.get("password") == request.form.get("password2"):
        return "ERR_PASSWORDS_DIFFERENT", 500
    short = request.form.get("short") if not request.form.get("short") == "" else None
    persistant = 1 if request.form.get("persistant") else 0
    smb_homedir = "/home/users/" + request.form.get("username")
    dbconn.execute("INSERT INTO people (id, firstname, lastname, preferredname, sex, title, short, email, birthdate, username, smb_homedir, persistant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, request.form.get("firstname"), request.form.get("lastname"), request.form.get("preferredname"), request.form.get("sex"), request.form.get("title"), short, request.form.get("email"), request.form.get("birthdate"), request.form.get("username"), smb_homedir, persistant))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    if not request.form.get("cleartext") is None:
        dbconn.execute("INSERT INTO userpassword (people_id, unix_hash, smb_hash, hint, cleartext, autogen) VALUES (%s, %s, %s, %s, %s, 1)", (id, hash.unix(request.form.get("password")), hash.samba(request.form.get("password")), request.form.get("pwhint"), request.form.get("password")))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
    else:
        dbconn.execute("INSERT INTO userpassword (people_id, unix_hash, smb_hash, hint, autogen) VALUES (%s, %s, %s, %s, 0)", (id, hash.unix(request.form.get("password")), hash.samba(request.form.get("password")), request.form.get("pwhint")))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
    failed = False
    for group in json.loads(request.form.get("groups")):
        dbconn.execute("INSERT INTO people_has_groups (people_id, group_id) VALUES (%s, %s)", (id, group))
        if not dbconn.commit():
            failed = True
        if not lg.addUser(id, group) == 0:
            failed = True
    if failed:
        return "ERR_DATABASE_ERROR", 500
    dircode = dir.create(request.form.get("username"), "users")
    if dircode == 0 and dir.setMode(request.form.get("username"), "users", "511"): # 511 in octal gives 777
        if not lu.update(id) == 0:
            return "ERR_LDAP_ERROR", 500
        dbconn.execute("SELECT unix_userid FROM people WHERE id = %s LIMIT 1", (id,))
        result = dbconn.fetchone()
        if not dir.setOwner(request.form.get("username"), "users", result["unix_userid"]):
            return "ERR_DATABASE_ERROR", 500
    elif dircode == -1:
        return "ERR_FOLDER_PLACE_INVALID", 500
    elif dircode == -4:
        return "ERR_FOLDER_EXISTS", 500
    else:
        return "ERR_CREATE_HOMEFOLDER", 500
    return "SUCCESS", 201

@userApi.route("/api/user/<id>/password", methods=["PUT"])
@login_required
def newPassword(id):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    lu = ldap.users()
    dbconn.execute("SELECT unix_hash FROM userpassword UP INNER JOIN people P ON UP.people_id = P.id WHERE P.id = %s", (id,))
    result = dbconn.fetchone()
    if not passlib.hash.ldap_salted_sha1.verify(request.form.get("old"), result["unix_hash"]):
        return "ERR_AUTH_PASSWORD", 500
    if not request.form.get("new1") == request.form.get("new2"):
        return "ERR_PASSWORDS_DIFFERENT", 500
    dbconn.execute("UPDATE userpassword SET unix_hash = %s, smb_hash = %s, hint = %s, autogen = 0, cleartext = NULL WHERE people_id = %s", (hash.unix(request.form.get("new1")), hash.samba(request.form.get("new1")), request.form.get("pwhint"), id))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    if not lu.update(id) == 0:
        return "ERR_LDAP_ERROR", 500
    return "SUCCESS", 200

@userApi.route("/api/user/<id>/resetpassword", methods=["PUT"])
@login_required
def resetPassword(id):
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    dbconn = db.database()
    lu = ldap.users()
    dbconn.execute("SELECT unix_hash FROM userpassword UP INNER JOIN people P ON UP.people_id = P.id WHERE P.username = %s", (current_user.username,))
    result = dbconn.fetchone()
    if not passlib.hash.ldap_salted_sha1.verify(request.form.get("authpassword"), result["unix_hash"]):
        return "ERR_AUTH_PASSWORD", 500
    if not request.form.get("password") == request.form.get("password2"):
        return "ERR_PASSWORDS_DIFFERENT", 500
    dbconn.execute("UPDATE userpassword SET unix_hash = %s, smb_hash = %s, hint = %s, cleartext = NULL, autogen = 0 WHERE people_id = %s", (hash.unix(request.form.get("password")), hash.samba(request.form.get("password")), request.form.get("pwhint"), id))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    if not lu.update(id) == 0:
        return "ERR_LDAP_ERROR", 500
    return "SUCCESS", 200
