#!/usr/bin/env python3

# SchoolConnect Backend
# Hash functions
# © 2020 Johannes Kreutz.

# Include dependencies
import hashlib
import passlib.hash

# Function definitions
def unix(input):
    return passlib.hash.ldap_salted_sha1.hash(input)

def samba(input):
    return passlib.hash.nthash.encrypt(input).upper()

def sha256(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()
