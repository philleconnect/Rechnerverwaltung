#!/usr/bin/env python3

# SchoolConnect Backend
# Essential functions
# © 2020 Johannes Kreutz.

# Include dependencies
import os
import random
from flask_login import current_user

# Include modules
import modules.permissionCheck as pCheck

# Essential functions
def getBasePath():
    return os.path.dirname(os.path.realpath(__file__)) + "/.."

def randomString(length = 10):
    letters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(letters) for i in range(length))

def isAuthorized(permissions):
    permissionCheck = pCheck.permissionCheck()
    return permissionCheck.check(current_user.username, permissions)
