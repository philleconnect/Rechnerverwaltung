#!/usr/bin/env python3

# SchoolConnect Backend
# Setup API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
import os
from flask import Blueprint, request

# Include modules
import config
import modules.database as db
import helpers.idservice as idsrv
import helpers.hash as hash
import modules.ldap as ldap
import modules.directory as directory
import modules.configfile as cf
import modules.ssh as ssh

# Endpoint definition
setupApi = Blueprint("setupApi", __name__)
# IPFire setup
@setupApi.route("/api/setup/ipfire", methods=["POST"])
def setupIPFire():
    if os.path.exists(config.CONFIG_IPFIRE_FILE):
        return "ERR_SETUP_ALREADY_DONE", 403
    else:
        if request.form.get("jump") == None:
            if not request.form.get("setup") == None:
                try:
                    sshConnection = ssh.ssh(request.form.get("url"), int(request.form.get("port")), "root", request.form.get("rootpassword"))
                    if sshConnection == False:
                        return "ERR_ROOT_PASSWORD_WRONG", 200
                except ValueError:
                    return "ERR_PORT_NOT_A_NUMBER", 400
                if not sshConnection.exec("useradd philleconnect"):
                    return "ERR_IPFIRE_SETUP_USERADD", 500
                if not sshConnection.exec("echo philleconnect:" + request.form.get("password") + " | chpasswd"):
                    return "ERR_IPFIRE_SETUP_SETPASS", 500
                if not sshConnection.exec("chmod =4755 /usr/local/bin/firewallctrl"):
                    return "ERR_IPFIRE_SETUP_PERMISSIONS", 500
                if not sshConnection.exec("chmod =666 /var/ipfire/fwhosts/customhosts"):
                    return "ERR_IPFIRE_SETUP_PERMISSIONS", 500
                if not sshConnection.exec("chmod =666 /var/ipfire/fwhosts/customgroups"):
                    return "ERR_IPFIRE_SETUP_PERMISSIONS", 500
                if not sshConnection.exec("mkdir /home/philleconnect"):
                    return "ERR_IPFIRE_SETUP_HOMEFOLDER", 500
                if not sshConnection.exec("mkdir /home/philleconnect/.ssh"):
                    return "ERR_IPFIRE_SETUP_SSHFILES", 500
                if not sshConnection.exec("chown -R philleconnect /home/philleconnect/"):
                    return "ERR_IPFIRE_SETUP_PERMISSIONS", 500
                if not sshConnection.put(config.CONFIG_BASE + "/ipfire/config", "/var/ipfire/firewall/input"):
                    return "ERR_IPFIRE_SETUP_RULES", 500
                sshConnection.close()
                sshConnection = ssh.ssh(request.form.get("url"), int(request.form.get("port")), "philleconnect", request.form.get("password"))
                if sshConnection == False:
                    return "ERR_SETUP_ERROR", 200
                if not sshConnection.put(config.CONFIG_BASE + "/id_rsa.pub", "/home/philleconnect/.ssh/authorized_keys"):
                    return "ERR_IPFIRE_SETUP_SSHKEY", 500
                if not sshConnection.exec("/usr/local/bin/firewallctrl"):
                    return "ERR_IPFIRE_SETUP_RELOAD", 500
                sshConnection.close()
            configfile = cf.configfile()
            configfile.set("ipfire", "url", request.form.get("url"))
            configfile.set("ipfire", "port", request.form.get("port"))
            configfile.set("ipfire", "password", request.form.get("password"))
        open(config.CONFIG_IPFIRE_FILE, "a").close()
        return "SUCCESS", 200

# Admin account creation
@setupApi.route("/api/setup/admin", methods=["POST"])
def setupAdmin():
    if os.path.exists(config.CONFIG_ADMINUSER_FILE):
        return "ERR_SETUP_ALREADY_DONE", 403
    else:
        dir = directory.directory()
        if dir.exists(request.form.get("user"), "users"):
            return "ERR_FOLDER_EXISTS", 500
        id = idsrv.getNew()
        dbconn = db.database()
        dbconn.execute("INSERT INTO people (id, firstname, lastname, username, email, smb_homedir, preferredname, persistant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id, request.form.get("firstname"), request.form.get("lastname"), request.form.get("user"), request.form.get("email"), "/home/users/" + request.form.get("user"), request.form.get("firstname") + " " + request.form.get("lastname"), 1))
        dbconn.execute("INSERT INTO userpassword (people_id, unix_hash, smb_hash, hint) VALUES (%s, %s, %s, %s)", (id, hash.unix(request.form.get("password")), hash.samba(request.form.get("password")), request.form.get("pwhint")))
        dbconn.execute("INSERT INTO people_has_groups (people_id, group_id) VALUES (%s, (SELECT id FROM groups WHERE name = 'root'))", (id,))
        if not dbconn.commit():
            return "ERR_DATABASE_ERROR", 500
        lu = ldap.users()
        if not lu.update(id) == 0:
            return "ERR_LDAP_ERROR", 500
        if not dir.create(request.form.get("user"), "users") == 0 and not dir.setMode(request.form.get("user"), "users", "511"):
            return "ERR_CREATE_HOMEFOLDER", 500
        dbconn.execute("SELECT unix_userid FROM people WHERE id = %s LIMIT 1", (id,))
        result = dbconn.fetchone()
        if not dir.setOwner(request.form.get("user"), "users", result["unix_userid"]):
            return "ERR_CREATE_HOMEFOLDER", 500
        open(config.CONFIG_ADMINUSER_FILE, "a").close()
        return "SUCCESS", 200

# Get setup status
@setupApi.route("/api/setup/status", methods=["GET"])
def getStatus():
    if not os.path.exists(config.CONFIG_IPFIRE_FILE):
        return "SETUP_IPFIRE", 200
    if not os.path.exists(config.CONFIG_ADMINUSER_FILE):
        return "SETUP_ADMIN", 200
    return "SETUP_DONE", 200
