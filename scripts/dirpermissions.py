#!/usr/bin/env python3

# SchoolConnect Admin-Backend - directory permission set script
# © 2019 Johannes Kreutz.

# Include dependencies
import sys
import os
import shutil

# Catch failure cases
if len(sys.argv) != 4:
    print("Wrong number of parameters.")
    sys.exit()
if os.geteuid() != 0:
    print("You need to run this script as root.")
    sys.exit()

# Store and validate arguments
path = sys.argv[2]
if ".." in path:
    print("Going back in the file system is not allowed.")
    sys.exit()
mode = int(sys.argv[3], 8)

# Run permission set
if sys.argv[1] == "chown":
    shutil.chown(path, user=mode, group="root")
elif sys.argv[1] == "chmod":
    os.chmod(path, mode)
else:
    print("Unknown operator.")
