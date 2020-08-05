#!/usr/bin/env python3

# SchoolConnect Backend
# Automatic initial setup for database and ldap (connection check)
# © 2020 Johannes Kreutz.

# Include dependencies
import os
import mysql.connector
from ldap3 import Server, Connection, ALL

# Include modules
import modules.configfile as cf
import modules.database as db
import modules.ldap as ldap
import helpers.samba as samba

# Class definition
class autosetup:
    def __init__(self):
        self.__config = cf.configfile()

    # Check the connection to the mysql / mariadb server
    def runDatabaseAutoSetup(self):
        try:
            database = mysql.connector.connect(
                host = self.__config.get("database", "url"),
                user = os.environ.get("MYSQL_USER"),
                passwd = os.environ.get("MYSQL_PASSWORD"),
                database = self.__config.get("database", "name")
            )
        except Exception as e:
            print(e)
            return False
        else:
            self.__config.set("database", "user", os.environ.get("MYSQL_USER"))
            self.__config.set("database", "password", os.environ.get("MYSQL_PASSWORD"))
            samba.update()
            return True

    # Check the connection to the openldap server
    def runLdapAutoSetup(self):
        ldapServer = Server(self.__config.get("ldap", "url"))
        baseDn = "dc=" + os.environ.get("SLAPD_DOMAIN1") + ",dc=" + os.environ.get("SLAPD_DOMAIN0")
        try:
            Connection(ldapServer, self.__config.get("ldap", "admindn") + "," + baseDn, os.environ.get("SLAPD_PASSWORD"), auto_bind=True)
        except Exception as e:
            print(e)
            return False
        else:
            self.__config.set("ldap", "password", os.environ.get("SLAPD_PASSWORD"))
            self.__config.set("ldap", "basedn", baseDn)
            dbconn = db.database()
            dbconn.execute("SELECT id FROM groups")
            ldapGroups = ldap.groups()
            failed = False
            for row in dbconn.fetchall():
                if not ldapGroups.create(row["id"]) == 0:
                    failed = True
            return not failed
