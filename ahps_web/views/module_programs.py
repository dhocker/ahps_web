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
from ahps_web import app
from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify
from ahps_web.models.room import get_rooms, get_room, insert_room, delete_room, update_room
from ahps_web.models.module import get_modules_for_room, get_module, insert_module, update_module_hdc, \
    update_module_dim_amount, update_module_name, delete_module, delete_room_modules, get_modules_for_house, \
    update_module_type, move_module_room, update_module_selected
from ahps_web.models.program import get_program, get_programs_for_module, insert_program, delete_program, \
    update_program, delete_module_programs
from ahps_web.models.house_programs import get_house_summary
from ahps_web.bll.download import Downloader
from ahps_web.bll.sun_data import get_sun_data
from ahps_web.models.house import get_current_house, get_houses, set_current_house, get_house, update_house, \
    insert_house, delete_house
from ahps_web.bll.x10_control import device_on, device_off, all_lights_off, all_lights_on
from ahps_web.bll.copy_house import copy_house as bll_copy_house
from flask.ext.user import login_required
# import view_helpers # register context processors
import json


@app.route('/modules/programs/<moduleid>', methods=['GET', 'POST'])
@login_required                                 # Use of @login_required decorator
def module_programs(moduleid):
    '''
    Show list of programs for the given module ID
    :param moduleid:
    :return:
    '''
    if request.method == 'GET':
        module = get_module(moduleid)
        programs = get_programs_for_module(moduleid)
        return render_template("module_programs.html", module=module, programs=programs)
    elif request.method == 'POST':
        if request.form.has_key('add-program'):
            moduleid = request.form["add-program"]
            insert_program(moduleid, "New Program")
            return redirect(url_for("module_programs", moduleid=moduleid))
    else:
        pass


@app.route('/modules/programs/edit_program/<programid>', methods=['GET', 'POST'])
@login_required                                 # Use of @login_required decorator
def edit_program(programid):
    # This is not particularly elegant but it is functional.
    # If there is a returnto arg we will set up to go back to that page.
    # If there is no returnto arg we will default to going back to the
    # module programs page.
    if request.args.has_key("returnto"):
        returnto = request.args["returnto"]
    else:
        returnto = None

    if request.method == 'GET':
        program = get_program(programid)
        moduleid = program["moduleid"]
        module = get_module(moduleid)

        if not returnto:
            returnto = url_for("module_programs", moduleid=moduleid)

        sun_data = get_sun_data(datetime.now())

        return render_template("program.html", module=module, program=program, sun_data=sun_data, returnto=returnto)

    elif request.method == 'POST' and request.form.has_key("save"):
        program = get_program(programid)
        moduleid = program["moduleid"]

        if not returnto:
            returnto = url_for("module_programs", moduleid=moduleid)

        # Save all program data

        program["name"] = request.form["program-name"]

        # Build program days string from from inputs
        wd = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        days = ""
        for d in range(0, 7):
            key = "dow" + str(d)
            if request.form.has_key(key):
                days += wd[d]
            else:
                days += '.'
        program["days"] = days

        program["start_action"] = request.form["start-action"]
        program["stop_action"] = request.form["stop-action"]

        program["start_trigger_method"] = request.form["start-trigger-method"]
        program["stop_trigger_method"] = request.form["stop-trigger-method"]

        program["start_time"] = request.form["start-time"]
        program["stop_time"] = request.form["stop-time"]

        if request.form.has_key("start-randomize"):
            v = request.form["start-randomize"]
            program["start_randomize"] = 1
        else:
            program["start_randomize"] = 0

        if request.form.has_key("stop-randomize"):
            v = request.form["stop-randomize"]
            program["stop_randomize"] = 1
        else:
            program["stop_randomize"] = 0

        program["start_offset"] = int(request.form["start-offset"])

        program["stop_offset"] = int(request.form["stop-offset"])

        if request.form.has_key("start-randomize-amount"):
            program["start_randomize_amount"] = int(request.form["start-randomize-amount"])
        if request.form.has_key("stop-randomize-amount"):
            program["stop_randomize_amount"] = int(request.form["stop-randomize-amount"])

        # Finally! Update the program record with all of the changes
        update_program(program)

        flash(program["name"] + " saved")

        return redirect(returnto)
    else:
        program = get_program(programid)
        moduleid = program["moduleid"]
        return redirect(url_for("module_programs", moduleid=moduleid))


@app.route('/modules/programs/remove_program/<moduleid>', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def remove_program(moduleid):
    programid = request.args["programid"]
    delete_program(programid)
    # return "Remove program called for moduleid/programid" + moduleid + "/" + programid;
    return redirect(url_for("module_programs", moduleid=moduleid))
