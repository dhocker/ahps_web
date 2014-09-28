#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright (C) 2014  Dave Hocker (email: AtHomeX10@gmail.com)
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
from ahps_web.database.connection import get_db


def get_program(programid):
    '''
    Get a program given its program ID
    :return: The program record as a dict. This is done to provide a
        mutable object that will support updates.
    '''
    db = get_db()
    cur = db.execute('select * from programs where programid=?', [programid])
    program = cur.fetchone()
    return program_to_dict(program)


def get_programs_for_module(moduleid):
    '''
    Get all programs for a given module
    :return: A list of programs
    '''
    db = get_db()
    cur = db.execute('select * from programs where moduleid=?', [moduleid])
    programs = cur.fetchall()
    return programs


def insert_program(moduleid, name):
    '''
    Insert a program record
    :return: True if record was created
    '''
    db = get_db()
    db.execute('insert into programs (moduleid, name) values (?,?)',
               [moduleid, name])
    db.commit()
    return True


def delete_program(programid):
    '''
    Delete a program record given its programid
    :return: True if record was deleted
    '''
    db = get_db()
    db.execute('delete from programs where programid=?', (programid,))
    db.commit()
    return True


def delete_module_programs(moduleid):
    '''
    Delete all programs for a given moduleid
    :param moduleid:
    :return:
    '''
    db = get_db()
    db.execute('delete from programs where moduleid=?', (moduleid,))
    db.commit()
    return True


def update_program(program):
    '''
    Update an entire program record from a key/value dict DHO
    :param program:
    :return:
    '''

    colnames = ""
    values = []
    for k, v in program.iteritems():
        if k != "programid":
            if len(colnames) > 0:
                colnames += ","
            colnames += "{0}=?".format(k)
            values.append(v)
    values.append(program["programid"])

    stmt = 'update programs set {0} where programid=?'.format(colnames)

    db = get_db()
    db.execute(stmt, values)
    db.commit()
    return True


def program_to_dict(row):
    '''
    Convert a row object to an equivalent dict where the column names are keys.
    The dict acts as a DHO.
    :param row:
    :return:
    '''

    d = {}
    # The row keys are the table column names
    for c in row.keys():
        d[c] = row[c]

    return d
