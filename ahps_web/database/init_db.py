'''
Utility for creating the database. This is the simplest way to deal with
migrations and DB changes. Simply delete the existing DB file and
rerun this script.

If something more sophisticated is required we'll solve the problem when needed!
'''


import os
from sqlite3 import dbapi2 as sqlite3

dbname = 'ahps_web.sqlite3'

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(dbname)
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = connect_db()
    with open('schema.sql' , mode='r') as f:
        print 'Executing initialization script'
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


if __name__ == "__main__":
    # Database creation. As a precaution we only
    # create the database if it does not exist.
    # To update the schema, first delete the existing database.
    if os.path.isfile(dbname):
        print ''
        print 'Database already exists.'
        print 'If you want to update the schema, delete {0} first.'.format(dbname)
        print ''
    else:
        print ''
        print('Initializing the database')
        init_db()
        print('Database initialized')
        print ''
