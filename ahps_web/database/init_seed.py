# coding=utf-8
#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright (C) 2014, 2015  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

#
# Utility for seeding the database. This is the simplest way to deal with
# migrations and DB changes. Simply delete the existing DB file and
# rerun the init+db.py and init_seed.py scripts.
#
# If something more sophisticated is required we'll solve the problem when needed!
#


import os
from sqlite3 import dbapi2 as sqlite3

dbname = 'ahps_web.sqlite3'

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(dbname)
    rv.row_factory = sqlite3.Row
    return rv


def seed_db():
    """Seeds the database."""
    db = connect_db()
    with open('seed.sql' , mode='r') as f:
        print 'Executing seed script...'
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


if __name__ == "__main__":
    # Database creation. As a precaution we only
    # create the database if it does not exist.
    # To update the schema, first delete the existing database.
    if os.path.isfile(dbname):
        print ''
        seed_db()
        print 'Seeding complete'
        print ''
    else:
        print ''
        print('Database does not exist. Use init_db.py to create it.')
        print ''
