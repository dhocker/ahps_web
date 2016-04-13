#!/usr/bin/python

#
# Generate a new secret key 
#

import uuid

key = str(uuid.uuid4()).replace('-', '')

fh = open('secret_key', "w")
fh.write(key)
fh.close()

print "New secret key stored in file 'secret_key'"
