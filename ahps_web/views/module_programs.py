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
from flask_login import login_required
from ahps_web.views.view_helpers import build_program_summary
import json


@app.route('/module/<moduleid>/programs/page', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def module_programs_page(moduleid):
    '''
    Show list of programs for the given module ID
    :param moduleid:
    :return:
    '''
    module = get_module(moduleid)
    return render_template("module_programs.html", module=module,
                           ngapp="ahps_web", ngcontroller="moduleProgramsController")


@app.route('/module/<moduleid>/program', methods=['POST'])
@login_required                                 # Use of @login_required decorator
def add_module_program(moduleid):
    '''
    Add an empty program to the given module ID
    :param moduleid:
    :return:
    '''
    insert_program(moduleid, "New Program")
    return ""


@app.route('/module/<moduleid>/programs', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def get_module_programs(moduleid):
    '''
    Show list of programs for the given module ID
    :param moduleid:
    :return:
    '''
    programs = get_programs_for_module(moduleid)
    for program in programs:
        program["program_summary"] = build_program_summary(program);
    return jsonify({"programs" : programs})


@app.route('/modules/program/<programid>/page', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def edit_program_page(programid):
    program = get_program(programid)
    moduleid = program["moduleid"]
    module = get_module(moduleid)
    sun_data = get_sun_data(datetime.now())

    # This is not particularly elegant but it is functional.
    # If there is a returnto arg we will set up to go back to that page.
    # If there is no returnto arg we will default to going back to the
    # module programs page.
    if "returnto" in request.args:
        returnto = request.args["returnto"]
    else:
        returnto = url_for("module_programs_page", moduleid=moduleid)

    return render_template("program.html", programid=programid, sun_data=sun_data, returnto=returnto, ngapp="ahps_web", ngcontroller="programController")


@app.route('/module/program/<programid>', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def get_program_data(programid):

    program = get_program(programid)
    moduleid = program["moduleid"]
    module = get_module(moduleid)

    return jsonify({"programdata": {"program": program, "module": module}})


@app.route('/module/program/<programid>', methods=['POST'])
@login_required                                 # Use of @login_required decorator
def save_edit_program(programid):
    program = get_program(programid)
    # moduleid = program["moduleid"]
    # data is the program object
    args = json.loads(request.data.decode())["data"]

    # Save all program data

    program["name"] = args["name"]

    program["days"] = args["days"]

    program["start_action"] = args["start_action"]
    program["stop_action"] = args["stop_action"]

    program["start_trigger_method"] = args["start_trigger_method"]
    program["stop_trigger_method"] = args["stop_trigger_method"]

    program["start_time"] = args["start_time"]
    program["stop_time"] = args["stop_time"]

    program["start_randomize"] = args["start_randomize"]

    program["stop_randomize"] = args["stop_randomize"]

    program["start_offset"] = int(args["start_offset"])

    program["stop_offset"] = int(args["stop_offset"])

    program["start_randomize_amount"] = int(args["start_randomize_amount"])
    program["stop_randomize_amount"] = int(args["stop_randomize_amount"])

    # Finally! Update the program record with all of the changes
    update_program(program)

    flash(program["name"] + " saved")

    return "Saved"


@app.route('/module/program/<programid>', methods=['DELETE'])
@login_required                                 # Use of @login_required decorator
def remove_program(programid):
    delete_program(programid)
    # return "Remove program called for moduleid/programid" + moduleid + "/" + programid;
    return ""
