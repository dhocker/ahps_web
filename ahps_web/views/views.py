from ahps_web import app
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from ahps_web.models.room import get_rooms, get_room
from ahps_web.models.module import get_modules_for_room


def is_logged_in():
    '''
    Session helper
    :return: True if admin user is logged
    '''
    return session.has_key('logged_in') and session['logged_in']


@app.route("/")
def root():
    return redirect(url_for('home'))


@app.route("/home")
def home():
    # login is required
    if is_logged_in():
        rooms = get_rooms()
        return render_template('home.html', rooms=rooms)

    # Force login
    return redirect(url_for('login'))


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


@app.route('/edit_modules', methods=['POST'])
def edit_modules():
    '''
    Edit the programs for a given room identified by roomid
    :return: html page
    '''

    if is_logged_in():
        if request.form.has_key("roomid"):
            # The key is the name of the input or button element
            modules = get_modules_for_room(request.form["roomid"])
            room = get_room(request.form["roomid"])
            # return "roomid {0} has {1} modules".format(request.form["roomid"], len(modules))
            return render_template('modules.html', room=room, modules=modules,
                                   house_codes=house_codes(), device_codes=device_codes())
        elif request.form.has_key("remove"):
            return "Remove roomid: {0}".format(request.form["remove"])
        elif request.form.has_key("add"):
            return "Add another room"
    else:
        return redirect(url_for('login'))

    return redirect(url_for('login'))

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