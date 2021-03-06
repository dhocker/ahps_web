#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright (C) 2014, 2015 Dave Hocker (email: AtHomeX10@gmail.com)
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
from ahps_web.models.room import delete_rooms


def get_current_house():
    '''
    Get the current house record
    :return: houseid
    '''
    db = get_db()
    cur = db.execute("select * from houses where current=1")
    row = cur.fetchone()
    current_house = row_to_dict(row)
    return current_house


def set_current_house(houseid):
    '''
    Set the current house id
    :return:
    '''
    db = get_db()
    # Safe reset of ALL records
    db.execute('update houses set current=0')
    # Elect the selected house
    db.execute('update houses set current=1 where houseid=?', [houseid])
    db.commit()
    return True


def get_houses():
    '''
    Return the set of all house records
    :return:
    '''
    db = get_db()
    cur = db.execute('select * from houses order by name asc')
    houses = cur.fetchall()
    lst = []
    for house in houses:
        lst.append(row_to_dict(house))
    return lst


def get_house(houseid):
    '''
    Return the house record for the given ID
    :return:
    '''
    db = get_db()
    cur = db.execute('select * from houses where houseid=?', [houseid])
    house = cur.fetchone()
    return row_to_dict(house)


def update_house(houseid, name):
    '''
    Update name for selected house record
    :return:
    '''
    db = get_db()
    cur = db.execute('update houses set name=? where houseid=?', [name, houseid])
    db.commit()
    return True


def insert_house(name):
    '''
    Insert a new house record
    :return:
    '''
    db = get_db()
    cur = db.execute('insert into houses (name) values (?)', [name])
    houseid = cur.lastrowid
    db.commit()
    return houseid


def delete_house(houseid):
    '''
    Delete a house record given its houseid
    :return: True if record was deleted
    '''

    # Cascading delete
    # Delete all rooms in the house.
    delete_rooms(houseid)

    # Then delete the house
    db = get_db()
    db.execute('delete from houses where houseid=?', (houseid,))
    db.commit()
    return True
