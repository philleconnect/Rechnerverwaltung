#!/usr/bin/env python3

# SchoolConnect Backend
# SSH wrapper module
# © 2020 Johannes Kreutz.

# Include dependencies
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException
from scp import SCPClient

# Class definition
class ssh:
    def __init__(self, url, port, username, password):
        self.__ssh = SSHClient()
        self.__ssh.load_system_host_keys()
        self.__ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.__ssh.connect(url, port=port, username=username, password=password)
        except AuthenticationException:
            return False

    # Run ssh command
    def exec(self, command):
        (stdin, stdout, stderr) = self.__ssh.exec_command(command)
        return True if stdout.channel.recv_exit_status() == 0 else False

    # Put file via scp
    def put(self, source, dest):
        with SCPClient(self.__ssh.get_transport()) as scp:
            scp.put(source, dest)
        return True

    # Close connection
    def close(self):
        self.__ssh.close()
