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
from flask import Flask, request, url_for, render_template, jsonify
from ahps_web.models.house import get_current_house, get_houses, set_current_house, get_house, update_house, \
    insert_house, delete_house
from ahps_web.models.house_programs import get_house_summary
from ahps_web.models.module import get_modules_for_house
from ahps_web.bll.copy_house import copy_house as bll_copy_house
from view_helpers import build_program_summary
from view_exception import ViewException
from flask.ext.user import login_required
import json


@app.route("/houses/page", methods=["GET"])
@login_required                                 # Use of @login_required decorator
def houses_page():
    return render_template("houses.html", ngapp="ahps_web", ngcontroller="housesController")


@app.route("/houses", methods=["GET"])
@login_required                                 # Use of @login_required decorator
def get_all_houses():
    all_houses = get_houses()
    return jsonify({"houses": all_houses})


@app.route("/houses", methods=["POST"])
@login_required                                 # Use of @login_required decorator
def add_house():
    insert_house("New House")
    return ""


@app.route("/houses/selected/<houseid>", methods=["PUT"])
@login_required                                 # Use of @login_required decorator
def select_house(houseid):
    set_current_house(houseid)
    return ""


@app.route("/house/<houseid>/page", methods=["GET"])
@login_required                                 # Use of @login_required decorator
def edit_house(houseid):
    house = get_house(houseid)
    return render_template("edit_house.html", house=house, ngapp="ahps_web", ngcontroller="editHouseController")


@app.route("/house/<houseid>", methods=["GET"])
@login_required                                 # Use of @login_required decorator
def get_house_by_id(houseid):
    house = get_house(houseid)
    return jsonify({"house": house})


@app.route("/house/<houseid>", methods=["POST"])
@login_required                                 # Use of @login_required decorator
def save_house(houseid):
    args = json.loads(request.data.decode())["data"]
    update_house(houseid, args["name"])
    return ""


@app.route("/house/<houseid>", methods=["DELETE"])
@login_required                                 # Use of @login_required decorator
def remove_house(houseid):
    # Can't remove current house
    current_house = get_house(houseid)
    if current_house["current"] != 0:
        # TODO Return an error
        raise ViewException("Can't remove the current house", status_code=400)

    delete_house(houseid)
    return ""


@app.route("/houses/duplicate/<houseid>", methods=["POST"])
@login_required                                 # Use of @login_required decorator
def copy_house(houseid):
    # Run the copying logic
    bll_copy_house(houseid)
    return ""


@app.route("/house/summary/page", methods=['GET'])
@login_required                                 # Use of @login_required decorator
def house_summary():
    return render_template("house_summary.html", ngapp="ahps_web", ngcontroller="houseSummaryController")


@app.route("/house/summary", methods=['GET'])
@login_required                                 # Use of @login_required decorator
def get_house_summary_data():
    programs = get_house_summary(get_current_house()["houseid"])
    for program in programs:
        program["program_summary"] = build_program_summary(program);
    return jsonify({"programs": programs})
