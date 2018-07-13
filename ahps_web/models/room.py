# coding: utf-8
#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright © 2014, 2018  Dave Hocker (email: AtHomeX10@gmail.com)
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
from ahps_web.models.module import delete_room_modules
from ahps_web.models.model_helpers import row_to_dict


def get_rooms(houseid):
    '''
    Get all rooms for a house in ascending order by name
    :return: A list of all rooms
    '''
    db = get_db()
    cur = db.execute('select roomid,name,description from rooms where houseid=? order by name asc', [houseid])
    rooms = cur.fetchall()
    lst = []
    for room in rooms:
        lst.append(row_to_dict(room))
    return lst


def get_room(roomid):
    '''
    Get a room record given its id
    :return: A list of all rooms
    '''
    db = get_db()
    cur = db.execute('select roomid,name,description from rooms where roomid=?', [roomid])
    room = cur.fetchall()[0]
    return room


def update_room(roomid, name, description):
    '''
    Update the name and description columns
    :param roomid:
    :param name:
    :param description:
    :return:
    '''
    db = get_db()
    db.execute('update rooms set name=?, description=? where roomid=?',
               [name, description, roomid])
    db.commit()
    return True


def insert_room(houseid, name, desc):
    '''
    Insert a room record
    :return: True if record was created
    '''
    db = get_db()
    cur = db.execute('insert into rooms (name,houseid,description) values (?, ?, ?)', [name, houseid, desc])
    roomid = cur.lastrowid
    db.commit()
    return roomid


def delete_room(roomid):
    '''
    Delete a room record given its roomid
    :return: True if record was deleted
    '''

    # Cascading delete.
    # Then delete all modules in the room.
    delete_room_modules(roomid)

    db = get_db()
    db.execute('delete from rooms where roomid=?', (roomid,))
    db.commit()
    return True


def delete_rooms(houseid):
    '''
    Delete all room records given a houseid
    :return: True if record was deleted
    '''

    # Cascading delete. Delete all rooms for each module
    rooms = get_rooms(houseid)
    for room in rooms:
        delete_room(room["roomid"])

    return True
