#!/usr/bin/env python3

# SchoolConnect Backend
# IPFire updater
# © 2020 Johannes Kreutz.

# Include dependencies
import os

# Include modules
import modules.database as db
import modules.configfile as cf
import modules.ssh as ssh

# Function definition
def updateIpfire():
    if os.path.exists("/tmp/customhosts"):
        os.remove("/tmp/customhosts")
    if os.path.exists("/tmp/customgroups"):
        os.remove("/tmp/customgroups")
    dbconn = db.database()
    dbconn.execute("SELECT lastknownIPv4, address, networklock FROM device D INNER JOIN hardwareidentifier HW ON HW.device_id = D.id")
    with open("/tmp/customhosts", "w") as customhosts:
        with open("/tmp/customgroups", "w") as customgroups:
            counter = 1
            for machine in dbconn.fetchall():
                customhosts.write(str(counter) + "," + machine["address"] + ",ip," + machine["lastknownIPv4"] + "/255.255.255.255\n")
                if machine["networklock"] == 0:
                    customgroups.write(str(counter) + ",blocked,," + machine["address"] + ",Custom Host\n")
    configfile = cf.configfile()
    sshConnection = ssh.ssh(configfile.get("ipfire", "url"), int(configfile.get("ipfire", "port")), "philleconnect", configfile.get("ipfire", "password"))
    if sshConnection == False:
        return False
    if not sshConnection.put("/tmp/customhosts", "/var/ipfire/fwhosts/customhosts"):
        return False
    if not sshConnection.put("/tmp/customgroups", "/var/ipfire/fwhosts/customgroups"):
        return False
    if not sshConnection.exec("/usr/local/bin/firewallctrl"):
        return False
    sshConnection.close()
    return True
