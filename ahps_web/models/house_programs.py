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
from model_helpers import row_to_dict


def get_house_summary(houseid):
    """
    Get a summary of all house programs. The intention is to show
    a summary picture of all of the programs for a given house.
    :param houseid:
    :return:
    """
    db = get_db()
    sql = "select houses.name as house_name, rooms.name as room_name, " +\
        "modules.name as module_name, modules.house_code, modules.device_code, programs.* from houses " + \
        "join rooms on rooms.houseid = houses.houseid " + \
        "join modules on modules.roomid = rooms.roomid " + \
        "join programs on programs.moduleid = modules.moduleid " + \
        "where houses.houseid=? order by rooms.name, modules.name"
    cur = db.execute(sql, [houseid])
    programs = cur.fetchall()

    program_list = []
    for row in programs:
        program_list.append(row_to_dict(row))

    return program_list
