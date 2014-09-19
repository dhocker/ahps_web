from ahps_web import app
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from ahps_web.models.room import get_rooms
from ahps_web.models.module import get_modules_for_room


class room:
    def __init__(self, name, hdc):
        self.name = name
        self.hdc = hdc


@app.route("/")
def root():
    return redirect(url_for('home'))


@app.route("/home")
def home():
    items = ["one", "two", "three", "four", "five"]
    kvlist = {"a": "a-value", "b": "b-value"}

    obj_list = []
    obj_list.append(room("Office", "a1"))
    obj_list.append(room("Living Room", "a2"))
    obj_list.append(room("Studio", "l1"))

    rooms = get_rooms()

    return render_template('home.html', rooms=rooms)


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
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/edit_modules', methods=['POST'])
def edit_modules():
    '''
    Edit the programs for a given room identified by roomid
    :return: html page
    '''

    if request.form.has_key("roomid"):
        # The key is the name of the input or button element
        modules = get_modules_for_room(request.form["roomid"])
        return "roomid {0} has {1} modules".format(request.form["roomid"], len(modules))
    elif request.form.has_key("remove"):
        return "Remove roomid: {0}".format(request.form["remove"])
    elif request.form.has_key("add"):
        return "Add another room"


if __name__ == "__main__":
    app.run('0.0.0.0')