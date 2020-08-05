#!/usr/bin/env python3

# SchoolConnect Backend
# Host IP API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
import os
from flask import Blueprint, request
from flask_login import login_required

# Include modules
import helpers.essentials as es

# Endpoint definition
hostApi = Blueprint("hostApi", __name__)
@hostApi.route("/api/host", methods=["GET"])
@login_required
def getHost():
    if not es.isAuthorized("usermgmt"):
        return "ERR_ACCESS_DENIED", 403
    host = os.environ.get("HOST_NETWORK_ADDRESS")
    if host == None:
        host = ""
    return host, 200
