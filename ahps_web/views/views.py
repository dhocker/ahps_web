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
from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from ahps_web.models.room import get_rooms, get_room, insert_room, delete_room, update_room
from ahps_web.models.module import get_modules_for_room, get_module, insert_module, update_module_hdc, \
    update_module_dim_amount, update_module_name, delete_module, delete_room_modules, get_modules_for_house, \
    update_module_type, move_module_room
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
import view_helpers # register context processors


@app.route("/")
@login_required                                 # Use of @login_required decorator
def root():
    return redirect(url_for('home'))


@app.route("/about")
def about():
    '''
    This is the only page that does not require login
    :return:
    '''
    return render_template("about.html")


@app.route("/houses", methods=["GET", "POST"])
@login_required                                 # Use of @login_required decorator
def houses():
    if request.method == "GET":
        all_houses = get_houses()
        return render_template("houses.html", houses=all_houses)
    elif request.method == "POST":
        insert_house("New House")
        return redirect(url_for("houses"))


@app.route("/houses/select_house/<houseid>", methods=["GET"])
@login_required                                 # Use of @login_required decorator
def select_house(houseid):
    set_current_house(houseid)
    return redirect(url_for("home"))


@app.route("/houses/edit_house/<houseid>", methods=["GET", "POST"])
@login_required                                 # Use of @login_required decorator
def edit_house(houseid):
    if request.method == "GET":
        house = get_house(houseid)
        return render_template("edit_house.html", house=house)
    elif request.method == "POST":
        update_house(houseid, request.form["house-name"])
        return redirect(url_for("houses"))


@app.route("/houses/remove_house/<houseid>", methods=["GET"])
@login_required                                 # Use of @login_required decorator
def remove_house(houseid):
    # Can't remove current house
    current_house = get_house(houseid)
    if current_house["current"] != 0:
        houses = get_houses()
        error = "Can't delete the current house"
        return render_template("houses.html", error=error, houses=houses)

    delete_house(houseid)
    return redirect(url_for("houses"))


@app.route("/houses/copy_house/<houseid>", methods=["GET"])
@login_required                                 # Use of @login_required decorator
def copy_house(houseid):
    # Run the copying logic
    bll_copy_house(houseid)

    # Return new list of houses
    houses = get_houses()
    return render_template("houses.html", houses=houses)


@app.route("/home", methods=['GET', 'POST'])
@login_required                                 # Use of @login_required decorator
def home():
    if request.method == 'GET':
        current_house = get_current_house()
        rooms = get_rooms(current_house["houseid"])
        return render_template('home.html', rooms=rooms, house=current_house)

    elif request.method == 'POST':
        button = request.form['button']

        if button == "save":
            roomid = request.form['roomid']
            room = get_room(roomid)
            # TODO Need model update methods
            update_room(roomid, request.form["room-name"], request.form['room-description'])
            flash("The \"{0}\" room was saved".format(request.form['room-name']))
            return redirect(url_for("home"))

        elif button == 'showmodules':
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
@login_required                                 # Use of @login_required decorator
def add_room():
    if request.method == 'GET':
        # For a GET request, return the add room page
        return render_template('add_room.html')
    elif request.method == 'POST':
        # The POST request sends the add room form contents
        if request.form["save"] == "save":
            # Save new room
            current_house = get_current_house()
            if request.form["name"]:
                insert_room(current_house["houseid"], request.form["name"], request.form["description"])
            else:
                error = 'Room name is a required field'
                return render_template('add_room.html', error=error)

        # Return to the home page (list of rooms)
        return redirect(url_for('home'))


@app.route("/house_summary", methods=['GET'])
@login_required                                 # Use of @login_required decorator
def house_summary():
    programs = get_house_summary(get_current_house()["houseid"])
    return render_template("house_summary.html", programs=programs)


@app.route('/modules/<roomid>', methods=['GET', 'POST'])
@login_required                                 # Use of @login_required decorator
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
            update_module_type(moduleid, request.form["module_type"])
            update_module_name(moduleid, request.form["module-name"])
            if request.form['module_type'] == 'house':
                update_module_hdc(moduleid, request.form["house_code"], "")
            else:
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
            if request.form['module_type'] != 'house':
                # Appliance or lamp
                if device_on(moduleid):
                    flash("{0} turned on".format(request.form['module_type']))
            else:
                # All lights on for house code
                if all_lights_on(moduleid):
                    flash("All lights turned on")

        elif button == 'off':
            if request.form['module_type'] != 'house':
                if device_off(moduleid):
                    flash("{0} turned off".format(request.form['module_type']))
            else:
                # All lights off for house code
                if all_lights_off(moduleid):
                    flash("All lights turned off")

        else:
            return "Unrecognized button action"

    modules = get_modules_for_room(roomid)
    room = get_room(roomid)
    all_rooms = get_rooms(get_current_house()["houseid"])
    return render_template('modules.html', room=room, modules=modules, rooms=all_rooms)


@app.route('/modules/edit_module', methods=['POST'])
@login_required                                 # Use of @login_required decorator
def edit_module():
    return 'Edit module'


@app.route('/modules/add_module', methods=['POST'])
@login_required                                 # Use of @login_required decorator
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
@login_required                                 # Use of @login_required decorator
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
@login_required                                 # Use of @login_required decorator
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


@app.route('/modules/move_module', methods=['POST'])
@login_required                                 # Use of @login_required decorator
def move_module():
    moduleid = request.form["moduleid"]
    new_roomid = request.form["new_room"]

    # Implement move to new room
    move_module_room(moduleid, new_roomid)

    return redirect(url_for('modules', roomid=new_roomid))


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
    if request.method == 'GET':
        program = get_program(programid)
        module = get_module(program["moduleid"])

        sun_data = get_sun_data(datetime.now())

        return render_template("program.html", module=module, program=program, sun_data=sun_data)

    elif request.method == 'POST' and request.form.has_key("save"):
        program = get_program(programid)
        moduleid = program["moduleid"]

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

        return redirect(url_for("module_programs", moduleid=moduleid))
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


@app.route('/download_programs', methods=["POST"])
@login_required                                 # Use of @login_required decorator
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


@app.route('/all_house_codes', methods=["GET"])
@login_required                                 # Use of @login_required decorator
def all_house_codes():
    house = get_current_house()
    modules = get_modules_for_house(house["houseid"])
    return render_template("all_house_codes.html", house=house, modules=modules)
