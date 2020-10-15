#!/usr/bin/env python3

# SchoolConnect Backend
# Updater
# © 2020 Johannes Kreutz.

# Include dependencies
import json

# Include modules
import modules.database as db

# Updater function
def runUpdate(previousVersion):
    if (compareVersions(previousVersion, "2.0.102") == 1):
        dbconn = db.database()
        dbconn.execute("INSERT INTO permission (name, info, detail) VALUES (\"Passwort selbst zurücksetzen\", \"Nutzer kann sein Passwort selbst zurücksetzen, wenn eine E-Mail Adresse eingetragen ist.\", \"emailrst\")")
        dbconn.execute("INSERT INTO permission (name, info, detail) VALUES (\"Gruppenlisten einsehen\", \"Nutzer kann für all seine Gruppen eine Liste der Mitglieder einsehen und laden.\", \"grouplst\")")
        dbconn.execute("CREATE TABLE IF NOT EXISTS `schoolconnect`.`mailreset` (`time` TIMESTAMP NOT NULL, `token` VARCHAR(512) NOT NULL, `people_id` VARCHAR(64) NOT NULL, PRIMARY KEY (`time`, `people_id`), UNIQUE INDEX `token_UNIQUE` (`token` ASC), INDEX `fk_mailreset_people1_idx` (`people_id` ASC), CONSTRAINT `fk_mailreset_people1` FOREIGN KEY (`people_id`) REFERENCES `schoolconnect`.`people` (`id`) ON DELETE CASCADE ON UPDATE CASCADE) ENGINE = InnoDB;")
        dbconn.commit()

# Compares version numbers
def compareVersions(self, v1, v2):
    l1 = v1.split(".")
    l2 = v2.split(".")
    for i in range(3):
        if int(l1[i]) > int(l2[i]):
            return -1
        elif int(l1[i]) < int(l2[i]):
            return 1
    return 0
