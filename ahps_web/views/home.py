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
from flask_login import login_required
import view_helpers # register context processors
import json


@app.route("/")
@login_required                                 # Use of @login_required decorator
def root():
    return redirect(url_for('home'))


@app.route("/home", methods=['GET', 'POST'])
@login_required                                 # Use of @login_required decorator
def home():
    if request.method == 'GET':
        current_house = get_current_house()
        return render_template('home.html', ngapp="ahps_web", ngcontroller="homeController", house=current_house)

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


@app.route("/home/rooms", methods=['GET'])
def get_all_rooms():
    """
    Return all of the rooms
    :return:
    """
    current_house = get_current_house()
    rooms = get_rooms(current_house["houseid"])
    return jsonify({"rooms" : rooms})


@app.route("/home/room/<roomid>", methods=['PUT'])
@login_required                                 # Use of @login_required decorator
def save_room(roomid):
    args = json.loads(request.data.decode())["data"]
    update_room(roomid, args["room-name"], args['room-desc'])
    return ""


@app.route("/home/room/<roomid>", methods=['DELETE'])
@login_required                                 # Use of @login_required decorator
def remove_room(roomid):
    # This is a cascading delete
    delete_room(roomid)
    return ""


@app.route('/home/room', methods=['GET'])
@login_required                                 # Use of @login_required decorator
def show_add_room():
    # For a GET request, return the add room page
    return render_template('add_room.html', ngapp="ahps_web", ngcontroller="addroomController")


@app.route('/home/room', methods=['POST'])
@login_required                                 # Use of @login_required decorator
def create_new_room():
    # Create new room
    args = json.loads(request.data.decode())["data"]
    current_house = get_current_house()
    insert_room(current_house["houseid"], args["name"], args["description"])
    return ""


@app.route('/home/download_programs', methods=["PUT"])
@login_required                                 # Use of @login_required decorator
def download_programs():
    '''
    This is the target of an AJAX call mainly from the home page.
    All of the actions and programs are downloaded to the AtHomePowerLine server.
    :return:
    '''

    downloader = Downloader()
    downloader.download_programs()

    result = "<p>Result code: {0}</p><p>Message: {1}</p>".format(downloader.summary_response["result-code"],
                                                    downloader.summary_response["message"])

    return result
