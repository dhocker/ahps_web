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

from ahps_web.models.house import insert_house, get_house
from ahps_web.models.room import get_rooms, insert_room
from ahps_web.models.module import get_modules_for_room, insert_module
from ahps_web.models.program import get_programs_for_module, insert_program_from_record


def copy_house(houseid):
    '''
    Make a deep copy of the given house (by id) including all
    rooms, modules and programs within the house.
    :param houseid:
    :return: Returns the id of the new house.
    '''

    # The algorithm used here may not be optimal, but it is simple
    # and gives good performance for a typical house. The alternative
    # was to use SQL statements to copy record sets using subqueries.
    # The SQL approach would work better for large house configurations
    # but that would be the exception.

    # Create a new house record
    src_house = get_house(houseid)
    new_houseid = insert_house("Copy of {}".format(src_house["name"]))

    # Copy all of the rooms from the src house
    src_rooms = get_rooms(houseid)
    for src_room in src_rooms:
        new_room_id = insert_room(new_houseid, src_room["name"], src_room["description"])

        # Copy the modules for the room
        src_modules = get_modules_for_room(src_room["roomid"])
        for src_module in src_modules:
            new_module_id = insert_module(new_room_id, src_module["module_type"], src_module["name"],
                                          src_module["house_code"], src_module["device_code"],
                                          src_module["dim_amount"])

            # Copy all of the programs for the module
            src_programs = get_programs_for_module(src_module["moduleid"])
            for src_program in src_programs:
                # Copy the source record substituting the new module id
                insert_program_from_record(src_program, new_module_id)

    return new_houseid