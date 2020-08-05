#!/usr/bin/env python3

# SchoolConnect Backend
# Main API server
# © 2020 Johannes Kreutz.

# Include dependencies
import sys
import os
import json
from flask import Flask, request, session, Response
from flask_session import Session
from flask_login import LoginManager, login_required
from datetime import timedelta

# Include modules
import config
import modules.configfile as cf
import helpers.essentials as es
import modules.autosetup as autos
import modules.apiUser as apiUser

# Run first setup
if not os.path.exists(config.CONFIG_AUTOSETUP_FILE):
    autosetup = autos.autosetup()
    if not autosetup.runDatabaseAutoSetup():
        print("Error accessing MySQL database. Exiting.")
        sys.exit()
    if not autosetup.runLdapAutoSetup():
        print("Error accessing LDAP server. Exiting.")
        sys.exit()
    open(config.CONFIG_AUTOSETUP_FILE, "a").close()

# Include endpoints
from endpoints.login import loginApi
from endpoints.setup import setupApi
from endpoints.userlist import userListApi
from endpoints.grouplist import groupListApi
from endpoints.user import userApi
from endpoints.group import groupApi
from endpoints.usergroup import userGroupApi
from endpoints.permission import permissionApi
from endpoints.sharelist import shareListApi
from endpoints.sharegroup import shareGroupApi
from endpoints.share import shareApi
from endpoints.ipfire import ipfireApi
from endpoints.servermanager import serverManagerApi
from endpoints.profilelist import profileListApi
from endpoints.profiles import profileApi
from endpoints.devicelist import deviceListApi
from endpoints.device import deviceApi
from endpoints.host import hostApi
from endpoints.integritycheck import integritycheckApi
from endpoints.public import publicApi

# Manager objects
api = Flask(__name__)
SESSION_TYPE = "filesystem"
SESSION_COOKIE_NAME = "SC_SESSION"
SESSION_COOKIE_SECURE = False # Set this to true for production (SSL required)
PERMANENT_SESSION_LIFETIME = 1200
api.config.from_object(__name__)
api.secret_key = es.randomString(40)
login_manager = LoginManager()
login_manager.init_app(api)
login_manager.needs_refresh_message = (u"Session timed out, please re-login")

@login_manager.user_loader
def load_user(user_id):
    return apiUser.apiUser(user_id)

# Set session timeout to 20 minutes
@api.before_request
def before_request():
    session.permanent = True
    api.permanent_session_lifetime = timedelta(minutes=20)

# Register blueprints
api.register_blueprint(loginApi)
api.register_blueprint(setupApi)
api.register_blueprint(userListApi)
api.register_blueprint(groupListApi)
api.register_blueprint(userApi)
api.register_blueprint(groupApi)
api.register_blueprint(userGroupApi)
api.register_blueprint(permissionApi)
api.register_blueprint(shareListApi)
api.register_blueprint(shareGroupApi)
api.register_blueprint(shareApi)
api.register_blueprint(ipfireApi)
api.register_blueprint(serverManagerApi)
api.register_blueprint(profileListApi)
api.register_blueprint(profileApi)
api.register_blueprint(deviceListApi)
api.register_blueprint(deviceApi)
api.register_blueprint(hostApi)
api.register_blueprint(integritycheckApi)
api.register_blueprint(publicApi)

# EASTER EGG
@api.route("/api/coffee", methods=["GET"])
def teapot():
    return "I'm a teapot", 418

# Create server
if __name__ == "__main__":
    api.run(debug=True, port=8080, threaded=True)
