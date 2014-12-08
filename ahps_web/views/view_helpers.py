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
from ahps_web.bll.sun_data import get_astral_data
from datetime import datetime, timedelta


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


@app.context_processor
def program_summary_formatter():
    '''
    Formats a module program into a human readable summary.
    :return:
    '''
    def program_summary(program):
        # Calculate effective start and stop times
        sun_data = get_astral_data(datetime.now())
        sunset = sun_data["sunset"]
        sunrise = sun_data["sunrise"]

        effective_start_time = "No Time"
        offset = timedelta(minutes=int(program["start_offset"]))
        if program["start_trigger_method"] == "sunset":
            effective_start_time = (sunset + offset).strftime("%I:%M%p")
        elif program["start_trigger_method"] == "sunrise":
            effective_start_time = (sunrise + offset).strftime("%I:%M%p")
        elif program["start_trigger_method"] == "clock-time":
            st = program["start_time"]
            start_time = datetime.strptime(program["start_time"], "%I:%M %p")
            effective_start_time = (start_time + offset).strftime("%I:%M%p")
        else:
            effective_start_time = "No Time"

        effective_stop_time = "No Time"
        offset = timedelta(minutes=int(program["stop_offset"]))
        if program["stop_trigger_method"] == "sunset":
            effective_start_time = (sunset + offset).strftime("%I:%M%p")
        elif program["stop_trigger_method"] == "sunrise":
            effective_stop_time = (sunrise + offset).strftime("%I:%M%p")
        elif program["stop_trigger_method"] == "clock-time":
            st = program["stop_time"]
            stop_time = datetime.strptime(program["stop_time"], "%I:%M %p")
            effective_stop_time = (stop_time + offset).strftime("%I:%M%p")
        else:
            effective_stop_time = "No Time"

        start = "Start: Method={0} Offset={1} EffectiveTime={2} Action={3}".format(program["start_trigger_method"],
            program["start_offset"],
            effective_start_time, program["start_action"])
        stop = "Stop: Method={0} Offset={1} EffectiveTime={2} Action={3}".format(program["stop_trigger_method"],
            program["stop_offset"],
            effective_stop_time, program["stop_action"])
        return start + "<br/>" + stop

    return dict(program_summary = program_summary)