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

from datetime import datetime
from ahps_web.models.module_programs import get_all_module_programs
from ahps_web.ahps_api.ahps_api import AHPSRequest
from configuration import Configuration


class Downloader():
    '''
    Download the module programs to the AtHomePowerlineServer. The module programs
    are broken into actions and timers.
    '''
    def __init__(self):
        self.ahps_request = None
        self.actions_response = None
        self.timers_response = None
        self.summary_response = None


    def download_programs(self):
        '''
        Download all programs to the AtHomePowerlineServer
        :return:
        '''
        self.ahps_request = AHPSRequest(Configuration.Server(), port=Configuration.Port())
        self.ahps_request.create_timers_request()
        self.ahps_request.create_actions_request()

        programs = get_all_module_programs()

        for program in programs:
            # Translate each program into a set of actions and timers
            self.translate_program(program)

        # Send the actions. If this was successful, send the timers.
        self.actions_response = self.ahps_request.send_actions_request()
        if self.actions_response["result-code"] == 0:
            self.timers_response = self.ahps_request.send_timers_request()
            self.summary_response = self.timers_response
        else:
            self.summary_response = self.actions_response

        return self.summary_response["result-code"] == 0


    def translate_program(self, program):
        # Create actions for this program
        # Note that action names MUST be unique. We use the
        # programid key for this purpose.
        # Start
        start_action = {}
        start_action["name"] = "Start-" + str(program["programid"])
        start_action["command"] = program["start_action"]
        start_action["dim-amount"] = str(program["start_dim_percent"])
        # Stop
        stop_action = {}
        stop_action["name"] = "Stop-" + str(program["programid"])
        stop_action["command"] = program["stop_action"]
        stop_action["dim-amount"] = str(program["stop_dim_percent"])

        self.ahps_request.add_action(start_action)
        self.ahps_request.add_action(stop_action)

        # Create a timer for this program
        timer = {}

        # Make name unique by pre-pending the programid
        timer["name"] = str(program["programid"]) + "-" + program["name"]

        timer["start-action"] = start_action["name"]
        timer["stop-action"] = stop_action["name"]

        timer["house-device-code"] = program["house_code"] + program["device_code"]

        timer["start-trigger-method"] = program["start_trigger_method"]
        timer["stop-trigger-method"] = program["stop_trigger_method"]

        # Format conversion is required
        start_time = datetime.strptime(program["start_time"], "%I:%M %p")
        stop_time = datetime.strptime(program["stop_time"], "%I:%M %p")
        timer["start-time"] = start_time.strftime("%H:%M")
        timer["stop-time"] = stop_time.strftime("%H:%M")

        timer["start-time-offset"] = program["start_offset"]
        timer["stop-time-offset"] = program["stop_offset"]

        timer["start-randomize"] = program["start_randomize"]
        timer["stop-randomize"] = program["stop_randomize"]

        timer["start-randomize-amount"] = program["start_randomize_amount"]
        timer["stop-randomize-amount"] = program["stop_randomize_amount"]

        timer["day-mask"] = program["days"]

        self.ahps_request.add_timer(timer)
