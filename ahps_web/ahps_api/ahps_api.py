# coding: utf-8
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

import socket
import sys
import json
import datetime
import time

class AHPSRequest:
    # TODO We'll need a configuration file to allow specification of server name and port.

    #######################################################################
    # Constructor of an instance
    def __init__(self, host, port=9999):
        self.actions = {}
        self.timers = {}
        self.host = host
        self.port = port


    #######################################################################
    # Create an empty server request
    # This is the safe way to create an empty request.
    # The json module seems to be a bit finicky about the
    # format of strings that it converts.
    @staticmethod
    def create_request(command):
        request = {}
        request["request"] = command
        # The args parameter is an dictionary.
        request["args"] = {}
        return request


    #######################################################################
    # Open a socket to the server
    # Note that a socket can only be used for one request.
    # The server seems to close the socket at when it is
    # finished handling the request.
    def connect_to_server(self):

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and check status
            sock.connect((self.host, self.port))
            return sock
        except Exception as ex:
            print("Unable to connect to server:", self.host, self.port)
            print(str(ex))

        return None


    # ######################################################################
    # Read a JSON payload from a socket
    @staticmethod
    def read_json(sock):
        depth = 0
        json_data = ""

        while (True):
            c = sock.recv(1).decode()
            json_data += c

            if (c == "{"):
                depth += 1
            if (c == "}"):
                depth -= 1
                if (depth == 0):
                    return json_data


    # ######################################################################
    # Display a formatted response on the console
    @staticmethod
    def display_response(response):
        jr = json.loads(response)["X10Response"]

        print("Response for request:", jr["request"])

        # Loop through all of the entries in the response dict
        for k, v in jr.items():
            if k != "request":
                print(" ", k, ":", v)
        print()


    #######################################################################
    # Send a command to the server
    def send_command(self, data):
        # Convert the payload structure into json text.
        # Effectively this serializes the payload.
        #print "raw json:", data
        json_data = json.JSONEncoder().encode(data)

        # Create a socket connection to the server
        sock = self.connect_to_server()
        if sock is None:
            return None

        # send status request to server
        try:
            print("Sending request:", json_data)
            sock.sendall(json_data.encode())

            # Receive data from the server and shut down
            json_data = AHPSRequest.read_json(sock)

            #print "Sent:     {}".format(data)
            #print "Received: {}".format(json_data)
            #DisplayResponse(json_data)
        except Exception as ex:
            print(str(ex))
            json_data = None
        finally:
            sock.close()

        return json.loads(json_data)["X10Response"]


    #######################################################################
    # Test the Get Time command
    def get_time(self):
        #
        data = AHPSRequest.create_request("GetTime")

        return self.send_command(data)


    #######################################################################
    # Test the Set Time command
    def set_time(self):
        #
        data = AHPSRequest.create_request("SetTime")

        return self.send_command(data)


    #######################################################################
    # Test the Device On command
    def device_on(self, house_device_code, dim_amount):
        #
        data = AHPSRequest.create_request("On")
        data["args"]["house-device-code"] = house_device_code
        data["args"]["dim-amount"] = dim_amount

        return self.send_command(data)


    #######################################################################
    # Test the Device Off command
    def device_off(self, house_device_code, dim_amount):
        #
        data = AHPSRequest.create_request("Off")
        data["args"]["house-device-code"] = house_device_code
        data["args"]["dim-amount"] = dim_amount

        return self.send_command(data)


    #######################################################################
    # Test the Device Dim command
    def device_dim(self, house_device_code, dim_amount):
        #
        data = AHPSRequest.create_request("Dim")
        data["args"]["house-device-code"] = house_device_code
        data["args"]["dim-amount"] = dim_amount

        return self.send_command(data)


    #######################################################################
    # Test the Device Bright command
    def device_bright(self, house_device_code, bright_amount):
        #
        data = AHPSRequest.create_request("Bright")
        data["args"]["house-device-code"] = house_device_code
        data["args"]["bright-amount"] = bright_amount

        return self.send_command(data)


    #######################################################################
    # Test the Device All Units Off command
    def device_all_units_off(self, house_code):
        #
        data = AHPSRequest.create_request("AllUnitsOff")
        data["args"]["house-code"] = house_code

        return self.send_command(data)


    #######################################################################
    # Test the Device All Light On command
    def device_all_lights_on(self, house_code):
        #
        data = AHPSRequest.create_request("AllLightsOn")
        data["args"]["house-code"] = house_code

        return self.send_command(data)


    #######################################################################
    # Test the Device All Light Off command
    def device_all_lights_off(self, house_code):
        #
        data = AHPSRequest.create_request("AllLightsOff")
        data["args"]["house-code"] = house_code

        return self.send_command(data)


    #######################################################################
    # Test the status request command
    def status_request(self):
        data = AHPSRequest.create_request("StatusRequest")

        return self.send_command(data)


    #######################################################################
    # Get sunset and sunrise time for a given date
    def get_sun_data(self, for_isodate):
        data = AHPSRequest.create_request("GetSunData")
        data["args"]["date"] = for_isodate

        result = self.send_command(data)

        return result


    #######################################################################
    # TODO We'll need to define the interface to this function
    def create_timers_request(self):
        self.timers = AHPSRequest.create_request("LoadTimers")

        # For the LoadTimers command, the args dictionary contains a single
        # "programs" key/value pair. The value is a simple sequence/list of dict's where each dict
        # defines a timer initiator program.
        self.timers["args"]["programs"] = []


    #######################################################################
    # TODO We'll need to define the interface to this function
    # See documentation at bottom on file
    def add_timer(self, timer):
        self.timers["args"]["programs"].append(timer)


    #######################################################################
    def send_timers_request(self):
        return self.send_command(self.timers)


    #######################################################################
    # TODO We'll need to define the interface to this function
    def create_actions_request(self):
        self.actions = AHPSRequest.create_request("LoadActions")

        # For the LoadTimers command, the args dictionary contains a single
        # "programs" key/value pair. The value is a simple sequence/list of dict's where each dict
        # defines a timer initiator program.
        self.actions["args"]["actions"] = []


    #######################################################################
    # TODO We'll need to define the interface to this function
    # See documentation at bottom on file
    def add_action(self, action):
        self.actions["args"]["actions"].append(action)


    #######################################################################
    def send_actions_request(self):
        return self.send_command(self.actions)


    # Taken from the AtHomePowerlineServer documentation
    # Structure of a LoadTimers request
    # data =
    # {
    #     “request”: “LoadTimers”,
    #     “args”:
    #             {
    #                 “programs”:
    #                     [
    #                         {                                         # one timer program
    #                             “name”: “program-name”,
    #                             “house-device-code”: “a1”,
    #                             “start-trigger-method”: “clock-time”,
    #                             “stop-trigger-method”: “clock-time”,
    #                             “start-time”: “15:30”,
    #                             “start-time-offset”: “10”,
    #                             “start-randomize”: “1”,
    #                             “start-randomize-amount”: “10”,
    #                             “stop-time”: “23:30”,
    #                             “stop-time-offset”: “-10”,
    #                             “stop-randomize”: “1”,
    #                             “stop-randomize-amount”: “10”,
    #                             “day-mask”: “mtwtfss”,
    #                             “start-action”: “action-name”,
    #                             “stop-action”: “action-name”
    #                         },
    #                         {
    #                             ...another timer program
    #                         }
    #                     ]
    #             }
    # }

    # Structure of LoadActions request
    # {
    # 	“request”: “LoadActions”,
    # 	“args”:
    # 			{
    # 				“actions”:
    # 					[
    # 						{                                           # one action
    # 							“name”: “action-name”,
    # 							“command”: “x10-command”,
    # 							“dim-amount”: “nn”
    # 						},
    # 						{
    # 							...
    # 						}
    # 					]
    # 			}
    # }
