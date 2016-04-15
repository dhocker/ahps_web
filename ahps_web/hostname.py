#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright (C) 2014, 2016  Dave Hocker (email: AtHomeX10@gmail.com)
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
import socket

def GetHostName():
  """
  Returns the current hostname
  """
  # Just go for the first token in the full hostname
  hn = socket.gethostname().split('.')
  return hn[0]


@app.context_processor
def get_hostname():
    '''
    Exposes the variable hostname to jinga2 teplate renderer.
    :return:
    '''
    return dict(hostname = GetHostName())