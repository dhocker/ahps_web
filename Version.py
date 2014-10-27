#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright (C) 2014  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
#######################################################################

from ahps_web import app

def GetVersion():
  """
  Returns the current app version
  """
  return "2014.0.0.3"


@app.context_processor
def get_version():
    '''
    Exposes the variable version to jinga2 teplate renderer.
    :return:
    '''
    return dict(version = GetVersion())