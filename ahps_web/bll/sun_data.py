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
from ahps_web.ahps_api.ahps_api import AHPSRequest
from configuration import Configuration


def get_sun_data(for_datetime):
    target_date = for_datetime.strftime("%Y-%m-%d")
    ahps_request = AHPSRequest(Configuration.Server(), port=Configuration.Port())

    try:
        sun_data_response = ahps_request.get_sun_data(target_date)
        if sun_data_response["result-code"] == 0:
            return sun_data_response["data"]
    except:
        pass

    # Error
    return { "sunrise": None, "sunset": None }