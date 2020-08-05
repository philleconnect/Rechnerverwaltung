#!/usr/bin/env python3

# SchoolConnect Backend
# API server configuration
# © 2020 Johannes Kreutz.

# Include dependencies
import os

# Base config file path
CONFIG_BASE = "/etc/pc_admin"

# Path to configuration file
CONFIG_FILE_PATH = CONFIG_BASE + "/config.txt"
CONFIG_APIKEY_PATH = CONFIG_BASE + "/apikey.txt"

# Setup status files
CONFIG_AUTOSETUP_FILE = CONFIG_BASE + "/.AutoSetupDone"
CONFIG_IPFIRE_FILE = CONFIG_BASE + "/.IPFireSetupDone"
CONFIG_ADMINUSER_FILE = CONFIG_BASE + "/.AdminSetupDone"
