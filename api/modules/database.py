#!/usr/bin/env python3

# SchoolConnect Backend
# Database wrapper
# © 2020 Johannes Kreutz.

# Include dependencies
import mysql.connector

# Include modules
import modules.configfile as cf

# Class definition
class database:
    def __init__(self):
        config = cf.configfile()
        self.__db = mysql.connector.connect(
            host = config.get("database", "url"),
            user = config.get("database", "user"),
            passwd = config.get("database", "password"),
            database = config.get("database", "name")
        )
        self.__cursor = self.__db.cursor(dictionary=True)

    # Execute SQL command
    def execute(self, sql, values = None):
        try:
            if values == None:
                self.__cursor.execute(sql)
            elif isinstance(values, list):
                self.__cursor.executemany(sql, values)
            else:
                self.__cursor.execute(sql, values)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    # Get all results
    def fetchall(self):
        return self.__cursor.fetchall()

    # Get one result
    def fetchone(self):
        return self.__cursor.fetchone()

    # Commit changes
    def commit(self):
        try:
            self.__db.commit()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    # Return last inserted id
    def getId(self):
        return self.__cursor.lastrowid
