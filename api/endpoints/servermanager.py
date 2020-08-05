#!/usr/bin/env python3

# SchoolConnect Backend
# ServerManager API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
import requests
import json
from flask import Blueprint, request
from flask_login import login_required

# Include modules
import config
import helpers.essentials as es

# Endpoint definition
serverManagerApi = Blueprint("serverManagerApi", __name__)
@serverManagerApi.route("/api/servermanager", methods=["POST"])
@login_required
def servermanager():
    if not es.isAuthorized("servmgmt"):
        return "ERR_ACCESS_DENIED", 403
    data = {}
    if request.form.get("data"):
        data = json.loads(request.form.get("data"))
    with open(config.CONFIG_APIKEY_PATH) as f:
        data["apikey"] = f.read()[:-1]
    try:
        r = requests.post(url = "http://192.168.255.255:49100" + request.form.get("url"), data = data)
    except:
        return "ERR_CONNECTION_ERROR", 500
    else:
        return r.text, 200
