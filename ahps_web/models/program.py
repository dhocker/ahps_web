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
from ahps_web.database.connection import get_db
from ahps_web.models.model_helpers import row_to_dict


def get_program(programid):
    '''
    Get a program given its program ID
    :return: The program record as a dict. This is done to provide a
        mutable object that will support updates.
    '''
    db = get_db()
    cur = db.execute('select * from programs where programid=?', [programid])
    program = cur.fetchone()
    return row_to_dict(program)


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
    cur = db.execute('insert into programs (moduleid, name) values (?,?)',
               [moduleid, name])
    programid = cur.lastrowid
    db.commit()
    return programid


def insert_program_from_record(program, new_moduleid):
    '''
    Insert a program record from a modified copy of the record
    :return: True if record was created
    '''
    # moduleid integer not null,
    # name text default '',
    # days text default '.......',
    # start_trigger_method text default 'none',
    # start_time text default '12:00 AM',
    # start_offset integer default 0,
    # stop_trigger_method text default 'none',
    # stop_time text default '12:00 AM',
    # stop_offset integer default 0,
    # start_randomize integer default 0,
    # stop_randomize integer default 0,
    # start_randomize_amount integer default 0,
    # stop_randomize_amount integer default 0,
    # start_action text default 'none',
    # stop_action text default 'none',
    # start_dim_percent integer default 0,
    # stop_dim_percent integer default 0

    db = get_db()
    cur = db.execute('''insert into programs (moduleid, name, days, start_trigger_method, start_time,
                     start_offset, stop_trigger_method, stop_time, stop_offset, start_randomize,
                     stop_randomize, start_randomize_amount, stop_randomize_amount, start_action,
                     stop_action, start_dim_percent, stop_dim_percent) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                     [new_moduleid,
                     program["name"],
                     program["days"],
                     program["start_trigger_method"],
                     program["start_time"],
                     program["start_offset"],
                     program["stop_trigger_method"],
                     program["stop_time"],
                     program["stop_offset"],
                     program["start_randomize"],
                     program["stop_randomize"],
                     program["start_randomize_amount"],
                     program["stop_randomize_amount"],
                     program["start_action"],
                     program["stop_action"],
                     program["start_dim_percent"],
                     program["stop_dim_percent"]]
                     )
    programid = cur.lastrowid
    db.commit()
    return programid


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

