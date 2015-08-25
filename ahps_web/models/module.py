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

from ahps_web.database.connection import get_db
from ahps_web.models.program import get_programs_for_module, delete_module_programs
from model_helpers import row_to_dict


def get_modules_for_room(roomid):
    '''
    Get all modules for a given room
    :return: A list of modules
    '''
    db =    get_db()
    cur = db.execute('select * from modules where roomid=?', [roomid])
    modules = cur.fetchall()
    lst = []
    for module in modules:
        lst.append(row_to_dict(module))
    return lst


def get_modules_for_house(houseid):
    '''
    Get all modules for a house
    :return: A list of modules sorted by house and device code
    '''
    db =    get_db()
    sql = "select rooms.houseid, rooms.name as room_name, modules.* from rooms " + \
        "join modules on modules.roomid = rooms.roomid " + \
        "where rooms.houseid=? " \
        "order by modules.house_code, modules.device_code"
    cur = db.execute(sql, [houseid])
    modules = cur.fetchall()
    return modules


def get_module(moduleid):
    '''
    Get a module record for a given moduleid
    :return: A list of modules
    '''
    db = get_db()
    cur = db.execute('select * from modules where moduleid=?', [moduleid])
    module = cur.fetchone()
    return module


def update_module_hdc(moduleid, house_code, device_code):
    '''
    Update the hdc for a given module record
    :param moduleid:
    :param house_code:
    :param device_code:
    :return:
    '''
    db = get_db()
    db.execute('update modules set house_code=?, device_code=? where moduleid=?',
               [house_code, device_code, moduleid])
    db.commit()
    return True


def update_module_dim_amount(moduleid, dim_amount):
    '''
    Update the dim amount for a given module record (viable only for lamp module)
    :param moduleid:
    :param dim_amount:
    :return:
    '''
    db = get_db()
    db.execute('update modules set dim_amount=? where moduleid=?',
               [dim_amount, moduleid])
    db.commit()
    return True


def update_module_name(moduleid, name):
    '''
    Update the module name for a given module record
    :param moduleid:
    :param name:
    :return:
    '''
    db = get_db()
    db.execute('update modules set name=? where moduleid=?',
               [name, moduleid])
    db.commit()
    return True


def update_module_type(moduleid, module_type):
    '''
    Update the module type for a given module record
    :param moduleid:
    :param name:
    :return:
    '''
    db = get_db()
    db.execute('update modules set module_type=? where moduleid=?',
               [module_type, moduleid])
    db.commit()
    return True


def update_module_selected(moduleid, selected):
    '''
    Update the selected status for a given module record
    :param moduleid:
    :param selected:
    :return:
    '''
    db = get_db()
    db.execute('update modules set selected=? where moduleid=?',
               [selected, moduleid])
    db.commit()
    return True


def insert_module(roomid, module_type, name, house_code, device_code, dim_amount=0):
    '''
    Insert a module record
    :return: True if record was created
    '''
    db = get_db()
    cur = db.execute('insert into modules (roomid, module_type, name, house_code, device_code, dim_amount) values (?,?,?,?,?,?)',
               [roomid, module_type, name, house_code, device_code, dim_amount])
    moduleid = cur.lastrowid
    db.commit()
    return moduleid


def delete_module(moduleid):
    '''
    Delete a module record given its moduleid
    :return: True if record was deleted
    '''

    # Cascading delete. Delete all programs for the module
    delete_module_programs(moduleid)

    db = get_db()
    db.execute('delete from modules where moduleid=?', (moduleid,))
    db.commit()
    return True


def delete_room_modules(roomid):
    '''
    Delete all module records given a roomid
    :return: True if record was deleted
    '''

    # Cascading delete. Delete all programs for each module
    modules = get_modules_for_room(roomid)
    for module in modules:
        delete_module(module["moduleid"])

    return True


def move_module_room(moduleid, roomid):
    '''
    Move a module to a different room. Essentially, this simply
    sets the roomid of the module to the new room's ID.
    :return: True if module was moved
    '''

    db = get_db()
    db.execute('update modules set roomid=? where moduleid=?', [roomid, moduleid])
    db.commit()
    return True
