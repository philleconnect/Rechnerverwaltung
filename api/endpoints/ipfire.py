#!/usr/bin/env python3

# SchoolConnect Backend
# IPFire API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required
from pexpect import pxssh

# Include modules
import helpers.essentials as es
import modules.configfile as cf
import helpers.ipfire as ipfire

# Endpoint definition
ipfireApi = Blueprint("ipfireApi", __name__)
@ipfireApi.route("/api/ipfire", methods=["GET", "PUT"])
@login_required
def ipfire():
    if not es.isAuthorized("servmgmt"):
        return "ERR_ACCESS_DENIED", 403
    config = cf.configfile()
    if request.method == "GET":
        data = {
            "url": config.get("ipfire", "url"),
            "port": config.get("ipfire", "port"),
            "password": config.get("ipfire", "password"),
        }
        return jsonify(data), 200
    elif request.method == "PUT":
        config.set("ipfire", "url", request.form.get("url"))
        config.set("ipfire", "port", request.form.get("port"))
        config.set("ipfire", "password", request.form.get("password"))
        return "SUCCESS", 200
