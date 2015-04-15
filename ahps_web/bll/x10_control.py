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

from ahps_web.ahps_api.ahps_api import AHPSRequest
from configuration import Configuration
from ahps_web.models.module import get_module


def device_on(moduleid):
    '''
    Turns an appliance or lamp module on
    :param moduleid:
    :return: Returns true if request was successful. Otherwise, returns false.
    '''

    module = get_module(moduleid)
    ahps_request = AHPSRequest(Configuration.Server(), port=Configuration.Port())
    response = ahps_request.device_on(module["house_code"] + module["device_code"], module["dim_amount"])
    return response["result-code"] == 0


def device_off(moduleid):
    '''
    Turns an appliance or lamp module off
    :param moduleid:
    :return: Returns true if request was successful. Otherwise, returns false.
    '''

    module = get_module(moduleid)
    ahps_request = AHPSRequest(Configuration.Server(), port=Configuration.Port())
    response = ahps_request.device_off(module["house_code"] + module["device_code"], module["dim_amount"])
    return response["result-code"] == 0


def all_lights_on(moduleid):
    '''
    Turns all lights on for a house code
    :param moduleid:
    :return: Returns true if request was successful. Otherwise, returns false.
    '''

    module = get_module(moduleid)
    ahps_request = AHPSRequest(Configuration.Server(), port=Configuration.Port())
    response = ahps_request.device_all_lights_on(module["house_code"])
    return response["result-code"] == 0


def all_lights_off(moduleid):
    '''
    Turns all lights off for a house code
    :param moduleid:
    :return: Returns true if request was successful. Otherwise, returns false.
    '''

    module = get_module(moduleid)
    ahps_request = AHPSRequest(Configuration.Server(), port=Configuration.Port())
    response = ahps_request.device_all_lights_off(module["house_code"])
    return response["result-code"] == 0
