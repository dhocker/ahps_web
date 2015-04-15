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
from model_helpers import row_to_dict


def get_all_module_programs(houseid):
    '''
    Get all programs with relevant module information for the specified house. This is
    all of the data required to download to the AtHomePowerlineServer.
    :return: A list of module programs where each row in the list is a dict.
    '''
    db = get_db()
    sql = "select houses.houseid, modules.house_code, modules.device_code, programs.* from houses " + \
        "join rooms on rooms.houseid = houses.houseid " + \
        "join modules on modules.roomid = rooms.roomid " + \
        "join programs on programs.moduleid = modules.moduleid " + \
        "where houses.houseid=?"
    cur = db.execute(sql, [houseid])
    programs = cur.fetchall()

    program_list = []
    for row in programs:
        program_list.append(row_to_dict(row))

    return program_list
