#!/usr/bin/env python3

# SchoolConnect Backend
# Integrity check process class
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Flask, jsonify

# Include modules
from modules.integritycheckManager import integritycheckManager

# Create Flask instance
integrityApi = Flask(__name__)

# Create integrity check manager object
icMan = integritycheckManager()

# Create routes
@integrityApi.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@integrityApi.route("/status", methods=["GET"])
def status():
    return jsonify({"response": icMan.getStatus()}), 200

@integrityApi.route("/run", methods=["PUT"])
def run():
    icMan.run()
    return "DONE", 200

@integrityApi.route("/results", methods=["GET"])
def results():
    return jsonify({"response": icMan.getResults()}), 200

@integrityApi.route("/lastRun", methods=["GET"])
def lastRun():
    return jsonify({"response": icMan.getLastRun()}), 200

@integrityApi.route("/removeError/<id>/<error>/<user>", methods=["DELETE"])
def removeError(id, error, user):
    if user == "0":
        icMan.removeError(int(id), error, False)
    else:
        icMan.removeError(id, error, True)
    return "DONE", 200

# Create server
if __name__ == "__main__":
    integrityApi.run(port=25252, threaded=True)
