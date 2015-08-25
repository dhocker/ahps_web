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


@app.route('/modules_page/<roomid>', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def get_modules_page(roomid):
    '''
    Show the modules for a given room
    :return:
    '''
    #modules = get_modules_for_room(roomid)
    room = get_room(roomid)
    all_rooms = get_rooms(get_current_house()["houseid"])
    return render_template('modules.html', room=room, rooms=all_rooms, ngapp="ahps_web", ngcontroller="modulesController")


@app.route('/modules/<roomid>', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def get_modules(roomid):
    modules = get_modules_for_room(roomid)
    return jsonify({"modules": modules})


@app.route('/modules/<moduleid>/state', methods=['PUT'])
@login_required                                 # Use of @login_required decorator
def set_module_state(moduleid):
    """
    Change state of module to on or off
    :param roomid:
    :return:
    """
    args = json.loads(request.data.decode())["data"]
    if args["state"] == "on":
        if device_on(moduleid):
            # Return success
            pass
        else:
            # Return error
            pass
    elif args["state"] == "off":
        if device_off(moduleid):
            # Return success
            pass
        else:
            # Return error
            pass
    else:
        # Return an error
        pass
    return ""


# @app.route('/modules/<roomid>', methods=['POST'])
# @login_required                                 # Use of @login_required decorator
# def post_modules(roomid):
#     '''
#     Show the modules page for a given room
#     :return:
#     '''
#     # Possible actions: Save, edit programs, remove, on, off
#     moduleid = request.form["moduleid"]
#     button = request.form["button"]
#
#     if button == 'save':
#         update_module_type(moduleid, request.form["module_type"])
#         update_module_name(moduleid, request.form["module-name"])
#         if request.form['module_type'] == 'house':
#             update_module_hdc(moduleid, request.form["house_code"], "")
#         else:
#             update_module_hdc(moduleid, request.form["house_code"], request.form["device_code"])
#         if request.form['module_type'] == 'lamp':
#             update_module_dim_amount(moduleid, request.form['dim_amount'])
#         flash('Module record saved')
#
#     elif button == 'editprograms':
#         return redirect(url_for("module_programs", moduleid=moduleid))
#
#     elif button == 'remove':
#         module = get_module(moduleid)
#         # This is a cascading delete
#         delete_module(moduleid)
#         flash("The \"{0}\" module was removed".format(module['name']))
#
#     elif button == 'on':
#         if request.form['module_type'] != 'house':
#             # Appliance or lamp
#             if device_on(moduleid):
#                 flash("{0} turned on".format(request.form['module_type']))
#         else:
#             # All lights on for house code
#             if all_lights_on(moduleid):
#                 flash("All lights turned on")
#
#     elif button == 'off':
#         if request.form['module_type'] != 'house':
#             if device_off(moduleid):
#                 flash("{0} turned off".format(request.form['module_type']))
#         else:
#             # All lights off for house code
#             if all_lights_off(moduleid):
#                 flash("All lights turned off")
#
#     else:
#         return "Unrecognized button action"
#
#     modules = get_modules_for_room(roomid)
#     room = get_room(roomid)
#     all_rooms = get_rooms(get_current_house()["houseid"])
#     return render_template('modules.html', room=room, modules=modules, rooms=all_rooms)


@app.route('/module/<moduleid>', methods=['PUT'])
@login_required                                 # Use of @login_required decorator
def put_module(moduleid):
    """
    Update a module
    :param moduleid:
    :return:
    """
    args = json.loads(request.data.decode())["data"]

    update_module_type(moduleid, args["module_type"])
    update_module_name(moduleid, args["name"])
    if args['module_type'] == 'house':
        update_module_hdc(moduleid, args["house_code"], "")
    else:
        update_module_hdc(moduleid, args["house_code"], args["device_code"])
    if args['module_type'] == 'lamp':
        update_module_dim_amount(moduleid, args['dim_amount'])

    return ""


@app.route('/module/<moduleid>', methods=['DELETE'])
@login_required                                 # Use of @login_required decorator
def delete_module(moduleid):
    # This is a cascading delete
    delete_module(moduleid)


@app.route('/modules/edit_module', methods=['POST'])
@login_required                                 # Use of @login_required decorator
def edit_module():
    return 'Edit module'


@app.route('/room/<roomid>/new_appliance_module', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def add_appliance_module(roomid):
    room = get_room(roomid)
    return render_template('new_appliance_module.html', roomid=room['roomid'], room_name=room['name'])


@app.route('/room/<roomid>/new_lamp_module', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def add_lamp_module(roomid):
    room = get_room(roomid)
    return render_template('new_lamp_module.html', roomid=room['roomid'], room_name=room['name'])


# @app.route('/modules/new_appliance_module', methods=['POST'])
# @login_required                                 # Use of @login_required decorator
# def new_appliance_module():
#     # Save or cancel
#     if request.form.has_key('save'):
#         # Save (insert) new module record
#         roomid = request.form['save']
#         insert_module(roomid, 'appliance', request.form['name'],
#                       request.form['house_code'], request.form['device_code'])
#     else:
#         roomid = request.form['cancel']
#
#     # After save or cancel return to modules for room
#     return redirect(url_for('modules', roomid=roomid))


# @app.route('/modules/new_lamp_module', methods=['POST'])
# @login_required                                 # Use of @login_required decorator
# def new_lamp_module():
#     # Save or cancel
#     if request.form.has_key('save'):
#         # Save (insert) new module record
#         roomid = request.form['save']
#         insert_module(roomid, 'lamp', request.form['name'],
#                       request.form['house_code'], request.form['device_code'],
#                       request.form['dim_amount'])
#     else:
#         roomid = request.form['cancel']
#
#     # After save or cancel return to modules for room
#     return redirect(url_for('modules', roomid=roomid))


@app.route('/modules/move_module', methods=['POST'])
@login_required                                 # Use of @login_required decorator
def move_module():
    moduleid = request.form["moduleid"]
    new_roomid = request.form["new_room"]

    # Implement move to new room
    move_module_room(moduleid, new_roomid)

    return redirect(url_for('modules', roomid=new_roomid))
