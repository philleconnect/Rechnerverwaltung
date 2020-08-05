#!/usr/bin/env python3

# SchoolConnect Backend
# Directory functions
# © 2020 Johannes Kreutz.

# Include dependencies
import os
import shutil
from subprocess import Popen, PIPE

# Class definition
class directory:
    def __init__(self):
        return None

    # Return root path for a given storage space
    def __evalRootPath(self, where):
        path = os.sep + "home" + os.sep
        if where == "users":
            return path + "users" + os.sep
        elif where == "shares":
            return path + "shares" + os.sep
        elif where == "deleted":
            return path + "deleted" + os.sep
        else:
            return -1

    # Remove a starting slash
    def __fixName(self, name):
        if name.startswith(os.sep):
            return name[1:end]
        return name

    # Create a new folder
    # name: Folder name / path of the root directory: String
    # where: name of the root directory (users, shares, deleted)
    def create(self, name, where):
        path = self.__evalRootPath(where)
        name = self.__fixName(name)
        if path == -1:
            return -1
        if os.path.exists(path + name):
            return -4
        else:
            try:
                os.makedirs(path + name)
            except:
                return -3
            else:
                return 0

    # Delete a file / folder
    # name: Folder name / path of the root directory: String
    # where: name of the root directory (users, shares, deleted)
    def delete(self, name, where):
        path = self.__evalRootPath(where)
        name = self.__fixName(name)
        if path == -1:
            return -1
        return self.__deleteRecursive(path + name)

    # Helper to clear folders
    def __deleteRecursive(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                return -2
        os.rmdir(folder)
        return 0

    # Move a folder / file to a new place
    # oldname: Folder name / path of the old directory: String
    # oldwhere: name of the old root directory (users, shares, images, updates, deleted): String
    # name: Folder name / path of the new directory: String
    # where: name of the new root directory (users, shares, images, updates, deleted): String
    def move(self, oldname, oldwhere, name, where):
        oldpath = self.__evalRootPath(oldwhere)
        path = self.__evalRootPath(where)
        oldname = self.__fixName(oldname)
        name = self.__fixName(name)
        if path == -1 or oldpath == -1:
            return -1
        if not os.path.exists(oldpath + oldname):
            return -2
        try:
            shutil.move(oldpath + oldname, path + name)
        except:
            return -3
        else:
            return 0

    # Check if a folder exists
    # name: Folder name / path of the directory: String
    # where: name of the root directory (users, shares, images, updates, deleted): String
    def exists(self, name, where):
        path = self.__evalRootPath(where)
        name = self.__fixName(name)
        return os.path.exists(path + name)

    # Set owner user and group for a given file
    # name: Folder name / path of the directory: String
    # where: name of the root directory (users, shares, images, updates, deleted): String
    # user: unix user uid: Integer
    def setOwner(self, name, where, user):
        return self.__dirPermissionHelper(name, where, True, str(user))

    # Sets access modes for a given file
    # name: Folder name / path of the directory: String
    # where: name of the root directory (users, shares, images, updates, deleted): String
    # user: unix user uid: Integer
    def setMode(self, name, where, mode):
        return self.__dirPermissionHelper(name, where, False, mode)

    # Helper to set permissions with extended rights
    def __dirPermissionHelper(self, name, where, own, data):
        path = self.__evalRootPath(where)
        name = self.__fixName(name)
        mode = "chown" if own else "chmod"
        process = Popen(["sudo", "/usr/local/bin/dirpermissions.py", mode, path + name, data], stdout=PIPE)
        out = process.stdout.readline().decode("utf-8")
        if "Wrong number of parameters." in out or "You need to run this script as root." in out or "Going back in the file system is not allowed." in out or "Unknown operator." in out:
            return False
        return True

    # Returns actual owner
    # name: Folder name / path of the directory: String
    # where: name of the root directory (users, shares, images, updates, deleted): String
    def getOwner(self, name, where):
        path = self.__evalRootPath(where)
        name = self.__fixName(name)
        return os.stat(path + name).st_uid
