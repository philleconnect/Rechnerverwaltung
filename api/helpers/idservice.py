#!/usr/bin/env python3

# SchoolConnect Backend
# User ID service
# © 2020 Johannes Kreutz.

# Include dependencies
import time

# Include modules
import modules.database as db
import helpers.hash as hash
import helpers.essentials as es

# Function definition
def getNew():
    dbconn = db.database()
    dbconn.execute("SELECT id FROM people")
    ids = []
    for (id) in dbconn.fetchall():
        ids.append(id)
    id = "NOT_AN_ID"
    while id == "NOT_AN_ID" or id in ids:
        id = hash.sha256(str(time.time()) + es.randomString())
    return id
