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
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from ahps_web.models.room import get_rooms, get_room, insert_room, delete_room
from ahps_web.models.module import get_modules_for_room, get_module, insert_module, update_module_hdc, \
    update_module_dim_amount, delete_module


def is_logged_in():
    '''
    Session helper
    :return: True if admin user is logged
    '''
    return session.has_key('logged_in') and session['logged_in']


@app.route("/")
def root():
    return redirect(url_for('home'))


@app.route("/home", methods=['GET', 'POST'])
def home():
    # login is required
    if not is_logged_in():
        # Force login
        return redirect(url_for('login'))

    if request.method == 'GET':
        rooms = get_rooms()
        return render_template('home.html', rooms=rooms)

    elif request.method == 'POST':
        button = request.form['button']

        if button == 'showmodules':
            roomid = request.form['roomid']
            return redirect(url_for('modules', roomid=roomid))

        elif button == 'remove':
            # TODO Consider adding "are you sure?" test here
            # The roomid to be deleted is the value of the remove key
            roomid = request.form['roomid']
            room = get_room(roomid)
            delete_room(roomid)
            flash("The \"{0}\" room was removed".format(room['name']))
            #flash("The room was removed")
            return redirect(url_for('home'))

        elif button == 'addroom':
            return redirect(url_for('add_room'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    g.user = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    if is_logged_in():
        session.pop('logged_in', None)
        flash('You were logged out')
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
            update_module_hdc(moduleid, request.form["house_code"], request.form["device_code"])
            if request.form['module_type'] == 'lamp':
                update_module_dim_amount(moduleid, request.form['dim_amount'])
            flash('Module record saved')
        elif button == 'editprograms':
            pass
        elif button == 'remove':
            # TODO Add "are you sure" check
            module = get_module(moduleid)
            delete_module(moduleid)
            flash("The \"{0}\" module was removed".format(module['name']))
        elif button == 'on':
            pass
        elif button == 'off':
            pass
        else:
            return "Unrecognized button action"

    modules = get_modules_for_room(roomid)
    room = get_room(roomid)
    return render_template('modules.html', room=room, modules=modules)


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


def house_codes():
    codes = []
    for hcx in range(0, 16):
        codes.append(chr(ord('A') + hcx))
    return codes


def device_codes():
    codes = []
    for dcx in range(1, 17):
        codes.append(str(dcx))
    return codes


if __name__ == "__main__":
    app.run('0.0.0.0')