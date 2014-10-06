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
from ahps_web import app
import os
import time
from datetime import datetime
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from ahps_web.models.room import get_rooms, get_room, insert_room, delete_room
from ahps_web.models.module import get_modules_for_room, get_module, insert_module, update_module_hdc, \
    update_module_dim_amount, update_module_name, delete_module, delete_room_modules
from ahps_web.models.program import get_program, get_programs_for_module, insert_program, delete_program, \
    update_program, delete_module_programs
from ahps_web.views.login_views import is_logged_in
from ahps_web.bll.download import Downloader
from ahps_web.bll.sun_data import get_sun_data
from ahps_web.models.house import get_current_house
from ahps_web.bll.x10_control import device_on, device_off
from Version import GetVersion


@app.route("/")
def root():
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template("about.html", version=GetVersion())


@app.route("/home", methods=['GET', 'POST'])
def home():
    # login is required
    if not is_logged_in():
        # Force login
        return redirect(url_for('login'))

    if request.method == 'GET':
        current_house = get_current_house()
        rooms = get_rooms(current_house["houseid"])
        return render_template('home.html', rooms=rooms, house=current_house)

    elif request.method == 'POST':
        button = request.form['button']

        if button == 'showmodules':
            roomid = request.form['roomid']
            return redirect(url_for('modules', roomid=roomid))

        elif button == 'remove':
            # The roomid to be deleted is the value of the remove key
            roomid = request.form['roomid']
            room = get_room(roomid)
            # This is a cascading delete
            delete_room(roomid)
            flash("The \"{0}\" room was removed".format(room['name']))
            #flash("The room was removed")
            return redirect(url_for('home'))

        elif button == 'addroom':
            return redirect(url_for('add_room'))


@app.route('/home/add_room', methods=['GET', 'POST'])
def add_room():
    # login is required
    if is_logged_in():
        if request.method == 'GET':
            # For a GET request, return the add room page
            return render_template('add_room.html')
        elif request.method == 'POST':
            # The POST request sends the add room form contents
            if request.form["save"] == "save":
                # Save new room
                if request.form["name"]:
                    insert_room(request.form["name"], request.form["description"])
                else:
                    error = 'Room name is a required field'
                    return render_template('add_room.html', error=error)

            # Return to the home page (list of rooms)
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/modules/<roomid>', methods=['GET', 'POST'])
def modules(roomid):
    '''
    Show the modules for a given room
    :return:
    '''

    if request.method == 'GET':
        # Show modules for the roomid
        pass
    elif request.method == 'POST':
        # Possible actions: Save, edit programs, remove, on, off
        moduleid = request.form["moduleid"]
        button = request.form["button"]

        if button == 'save':
            update_module_name(moduleid, request.form["module-name"])
            update_module_hdc(moduleid, request.form["house_code"], request.form["device_code"])
            if request.form['module_type'] == 'lamp':
                update_module_dim_amount(moduleid, request.form['dim_amount'])
            flash('Module record saved')

        elif button == 'editprograms':
            return redirect(url_for("module_programs", moduleid=moduleid))

        elif button == 'remove':
            module = get_module(moduleid)
            # This is a cascading delete
            delete_module(moduleid)
            flash("The \"{0}\" module was removed".format(module['name']))

        elif button == 'on':
            if device_on(moduleid):
                flash("Module turned on")

        elif button == 'off':
            if device_off(moduleid):
                flash("Module turned off")

        else:
            return "Unrecognized button action"

    modules = get_modules_for_room(roomid)
    room = get_room(roomid)
    return render_template('modules.html', room=room, modules=modules)


@app.route('/modules/edit_module', methods=['POST'])
def edit_module():
    return 'Edit module'


@app.route('/modules/add_module', methods=['POST'])
def add_module():
    # The target room where the module is to be added is the value of the button that
    # was clicked.
    if request.form.has_key("add-appliance"):
        room = get_room(request.form['add-appliance'])
        return render_template('new_appliance_module.html', roomid=room['roomid'], room_name=room['name'])
    elif request.form.has_key("add-lamp"):
        room = get_room(request.form['add-lamp'])
        return render_template('new_lamp_module.html', roomid=room['roomid'], room_name=room['name'])
    return 'Unrecognized module type (neither appliance nor lamp)'


@app.route('/modules/new_appliance_module', methods=['POST'])
def new_appliance_module():
    # Save or cancel
    if request.form.has_key('save'):
        # Save (insert) new module record
        roomid = request.form['save']
        insert_module(roomid, 'appliance', request.form['name'],
                      request.form['house_code'], request.form['device_code'])
    else:
        roomid = request.form['cancel']

    # After save or cancel return to modules for room
    return redirect(url_for('modules', roomid=roomid))


@app.route('/modules/new_lamp_module', methods=['POST'])
def new_lamp_module():
    # Save or cancel
    if request.form.has_key('save'):
        # Save (insert) new module record
        roomid = request.form['save']
        insert_module(roomid, 'lamp', request.form['name'],
                      request.form['house_code'], request.form['device_code'],
                      request.form['dim_amount'])
    else:
        roomid = request.form['cancel']

    # After save or cancel return to modules for room
    return redirect(url_for('modules', roomid=roomid))


@app.route('/modules/programs/<moduleid>', methods=['GET', 'POST'])
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
def edit_program(programid):
    if request.method == 'GET':
        program = get_program(programid)
        module = get_module(program["moduleid"])

        sun_data = get_sun_data(datetime.now())

        return render_template("program.html", module=module, program=program, sun_data=sun_data)

    elif request.method == 'POST' and request.form.has_key("save"):
        program = get_program(programid)
        moduleid = program["moduleid"]

        # TODO Implement save

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

        return redirect(url_for("module_programs", moduleid=moduleid))
    else:
        program = get_program(programid)
        moduleid = program["moduleid"]
        return redirect(url_for("module_programs", moduleid=moduleid))


@app.route('/modules/programs/remove_program/<moduleid>', methods=['GET'])
def remove_program(moduleid):
    programid = request.args["programid"]
    delete_program(programid)
    # return "Remove program called for moduleid/programid" + moduleid + "/" + programid;
    return redirect(url_for("module_programs", moduleid=moduleid))


@app.route('/download_programs', methods=["POST"])
def download_programs():
    '''
    This is the target of an AJAX call mainly from the home page.
    All of the actions and programs are downloaded to the AtHomePowerLine server.
    :return:
    '''

    # TODO Implement download
    downloader = Downloader()
    downloader.download_programs()

    result = "<p>Result code: {0}</p><p>Message: {1}</p>".format(downloader.summary_response["result-code"],
                                                    downloader.summary_response["message"])

    return result
