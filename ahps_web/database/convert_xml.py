#!/usr/bin/python

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
# To convert an existing AtHomeX10 XML file:
#   workon flask            # Establish working virtual environment with Flask
#   python convert_xml.py name.xml

from xml.dom.minidom import parse
import xml.dom.minidom
import sys
import io
import os
import copy
from sqlite3 import dbapi2 as sqlite3
from init_db import init_db


# Keys are the DOM attribute name. Values are the table column name

room_kv = {
    "name": "name"
}
room_const = {
    "houseid": 0
}

module_kv = {
    "name": "name",
    "module-type": "module_type",
    "house-code": "house_code",
    "device-code": "device_code"
}
module_const = {
    "roomid": 0
}

program_kv = {
    "days": "days",
    "start-trigger-method": "start_trigger_method",
    "start-time": "start_time",
    # "start-sunset-offset": "start_offset",
    # "start-sunrise-offset": "start_offset", # TODO resolve multiple use
    "stop-trigger-method": "stop_trigger_method",
    "stop-time": "stop_time",
    # "stop-sunset-offset": "stop_offset",
    # "stop-sunrise-offset": "stop_offset", # TODO resolve multiple use
    "start-randomize": "start_randomize",
    "stop-randomize": "stop_randomize",
    "start-randomize-amount": "start_randomize_amount",
    "stop-randomize-amount": "stop_randomize_amount",
    "start-action": "start_action",
    "stop-action": "stop_action",
    "start-dim-percent": "start_dim_percent",
    "stop-dim-percent": "stop_dim_percent"
}
program_const = {
    "moduleid": 0
}


def create_db():
    """
    Opens the conversion database.
    Always starts with a new, empty database by deleting any existing one.
    """
    db_name = "ahps_web.sqlite3"

    # Check for DB existence. If it does not exist, create a new
    # DB. If it does exist, just open the existing DB file. This
    # way we can incrementally add existing house files to the DB.

    if not os.path.exists(db_name):
        init_db()

    rv = sqlite3.connect(db_name)
    rv.row_factory = sqlite3.Row

    return rv


def insert_db(db, sql):
    print sql
    cursor = db.cursor()
    cursor.execute(sql)
    inserted_id = cursor.lastrowid
    cursor.close()
    db.commit()
    return inserted_id


def insert_row(db, table_name, kv_map, const_map, dom_node):
    cols = ""
    vals = ""
    # k is the DOM attribute, v is the table column name.
    for k, v in kv_map.iteritems():
        if len(cols):
            cols += ","
            vals += ","
        cols += v
        # escape single quotes
        vals += "'" + dom_node.getAttribute(k).replace("'", "''") + "'"

    if const_map != None:
        for k, v in const_map.iteritems():
            cols += ","
            vals += ","
            cols += k
            # escape single quotes
            vals += str(v)

    sql = "insert into {0} ({1}) values ({2})".format(table_name, cols, vals)
    return insert_db(db, sql)


def convert_program(program, moduleid, db):
    days = program.getAttribute("days")
    print "    ", days

    # insert program for module
    # determine offset source based on trigger method for start and stop
    program_kv_copy = program_kv
    if program.getAttribute("start-trigger-method") == "sunset":
        program_kv_copy["start-sunset-offset"] = "start_offset"
    elif program.getAttribute("start-trigger-method") == "sunrise":
        program_kv_copy["start-sunrise-offset"] = "start_offset"
    if program.getAttribute("stop-trigger-method") == "sunset":
        program_kv_copy["stop-sunset-offset"] = "stop_offset"
    elif program.getAttribute("stop-trigger-method") == "sunrise":
        program_kv_copy["stop-sunrise-offset"] = "stop_offset"

    program_const["moduleid"] = moduleid

    programid = insert_row(db, "programs", program_kv_copy, program_const, program)


def convert_device(device, roomid, db):
    device_name = device.getAttribute("name")
    print "  ", device_name

    # insert device as module
    module_const["roomid"] = roomid
    moduleid = insert_row(db, "modules", module_kv, module_const, device)
    # get moduleid

    programs = device.getElementsByTagName("program")
    for program in programs:
        convert_program(program, moduleid, db)


def convert_room(room, houseid, db):
    room_name = room.getAttribute("name")
    print room_name

    # insert room
    room_const["houseid"] = houseid
    roomid = insert_row(db, "rooms", room_kv, room_const, room)
    # get roomid

    devices = room.getElementsByTagName("device")
    for device in devices:
        convert_device(device, roomid, db)


#
# main
#
if __name__ == "__main__":
    xml_file = sys.argv[1]
    dom = xml.dom.minidom.parse(xml_file)

    db = create_db()

    house = dom.documentElement

    # Insert house
    sql = "insert into houses (name) values ('{0}')".format(xml_file)
    # get houseid
    houseid = insert_db(db, sql)

    # Get all of the rooms in the house document element
    rooms = house.getElementsByTagName("room")
    for room in rooms:
        convert_room(room, houseid, db)

    # Make houseid the current house
    sql = "update houses set current=1 where houseid=1"
    db.execute(sql)
    db.commit()

    db.close()


# <room name="Craft Room">
#   <device module-type="appliance" name="Light, Wreath, Candles" house-code="B" device-code="5" x="8" y="7">
#     <program days="MTWTFSS" start-trigger-method="sunset" start-time="7:15 PM" start-sunset-offset="-20"
#       start-sunrise-offset="0" stop-trigger-method="clock-time" stop-time="10:05 PM" stop-sunset-offset="0"
#       stop-sunrise-offset="0" start-randomize="0" stop-randomize="0" start-randomize-amount="0"
#       stop-randomize-amount="0" start-action="on" stop-action="off" start-dim-percent="0" stop-dim-percent="0" />
#   </device>
# </room>
