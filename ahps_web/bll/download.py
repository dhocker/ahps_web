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

from ahps_web.models.module_programs import get_all_module_programs
from ahps_web.ahps_api.ahps_api import AHPSRequest
from configuration import Configuration


class Downloader():
    def __init__(self):
        pass


    def download_programs(self):
        '''
        Download all programs to the AtHomePowerlineServer
        :return:
        '''
        ahps_request = AHPSRequest(Configuration.Server(), port=Configuration.Port())
        ahps_request.create_timers_request()
        ahps_request.create_actions_request()

        programs = get_all_module_programs()

        self.actions = []
        self.timers = []

        for program in programs:
            # Translate each program into a set of actions and timers
            self.translate_program(program)

        # resp_a = ahps_request.send_actions_request()
        # resp_t = ahps_request.send_timers_request()

        return True


    def translate_program(self, program):
        # Create actions for this program
        # Start
        start_action = {}
        start_action["name"] = "Start-" + str(program["programid"])
        start_action["command"] = program["start_action"]
        start_action["dim-amount"] = program["start_dim_percent"]
        # Stop
        stop_action = {}
        stop_action["name"] = "Stop-" + str(program["programid"])
        stop_action["command"] = program["stop_action"]
        stop_action["stop_dim_percent"] = program["stop_dim_percent"]

        self.actions.append(start_action)
        self.actions.append(stop_action)

        # Create a timer for this program
        timer = {}
        timer["start-action"] = start_action["name"]
        timer["stop-action"] = stop_action["name"]

        timer["house-device-code"] = program["house_code" + program["device_code"]]

        timer["start-trigger-method"] = program["start_trigger_method"]
        timer["stop-trigger-method"] = program["stop_trigger_method"]

        timer["start-time"] = program["start_time"]
        timer["stop-time"] = program["stop_time"]

        if program["start_trigger_method"] == "sunset":
            timer["start-time-offset"] = program["start_sunset_offset"]
        elif program["start_trigger_method"] == "sunrise":
            timer["start-time-offset"] = program["start_sunrise_offset"]

        if program["stop_trigger_method"] == "sunset":
            timer["stop-time-offset"] = program["stop_sunset_offset"]
        elif program["stop_trigger_method"] == "sunrise":
            timer["stop-time-offset"] = program["stop_sunrise_offset"]

        pass