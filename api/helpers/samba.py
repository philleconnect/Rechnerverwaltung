#!/usr/bin/env python3

# SchoolConnect Backend
# Samba container share updater
# © 2020 Johannes Kreutz.

# Include dependencies
import mysql.connector
import requests
import json

# Include modules
import modules.database as db

# Function definition
def update():
    shares = []
    dbconn = db.database()
    dbconn.execute("SELECT name, path, id FROM shares")
    for share in dbconn.fetchall():
        dbconn.execute("SELECT G.name, GHS.permission FROM groups G INNER JOIN groups_has_shares GHS ON GHS.group_id = G.id WHERE GHS.shares_id = %s", (share["id"],))
        read = []
        write = []
        for permission in dbconn.fetchall():
            read.append(permission["name"])
            if permission["permission"] == 1:
                write.append(permission["name"])
        shares.append({
            "name": share["name"],
            "path": share["path"],
            "users": read,
            "write": write,
        })
    r = requests.post(url = "http://samba:8000", data = json.dumps(shares))
    if "Thanks, it worked" in r.text:
        return True
    return False
