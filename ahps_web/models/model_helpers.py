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


def row_to_dict(row):
    '''
    Convert a row object to an equivalent dict where the column names are keys.
    The dict acts as a DHO.
    :param row:
    :return:
    '''

    d = {}
    # The row keys are the table column names
    for c in row.keys():
        d[c] = row[c]

    return d
