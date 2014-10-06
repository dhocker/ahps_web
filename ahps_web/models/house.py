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
from ahps_web.models.model_helpers import row_to_dict


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
    cur = db.execute('select * from houses')
    houses = cur.fetchall()
    return row_to_dict(houses)
