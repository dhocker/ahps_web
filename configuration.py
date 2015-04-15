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

#
# App configuration
#
# The ahps_web.conf file holds the configuration data in JSON format.
# Currently, it looks like this:
#
# {
# "Configuration":
#   {
#     "DatabasePath": "/path/to/database/file",
#     "Server": "hostname",
#     "Port": "9999"
#   }
# }
#
# The JSON parser is quite finicky about strings being quoted as shown above.
#
# This class behaves like a singleton class. There is only one instance of the configuration.
# There is no need to create an instance of this class, as everything about it is static.
#

import os
import json
import logging

logger = logging.getLogger("app")

########################################################################
class Configuration():
    ActiveConfig = None
    AppPath = ""

    ######################################################################
    def __init__(self):
        Configuration.load_configuration()
        pass

    ######################################################################
    # Load the configuration file
    @classmethod
    def load_configuration(cls, app_path):
        if not app_path.endswith("/"):
            Configuration.AppPath = app_path + "/"
        else:
            Configuration.AppPath = app_path

        # Try to open the conf file. If there isn't one, we give up.
        try:
            cfg_path = Configuration.get_configuration_file_path()
            logger.info("Opening configuration file {0}".format(cfg_path))
            cfg = open(cfg_path, 'r')
        except Exception as ex:
            logger.error("Unable to open {0}".format(cfg_path))
            logger.error(str(ex))
            return

        # Read the entire contents of the conf file
        cfg_json = cfg.read()
        cfg.close()
        #print cfg_json

        # Try to parse the conf file into a Python structure
        try:
            config = json.loads(cfg_json)
            # The interesting part of the configuration is in the "Configuration" section.
            cls.ActiveConfig = config["Configuration"]
        except Exception as ex:
            logger.error("Unable to parse configuration file as JSON")
            logger.error(str(ex))
            return

        #print str(Configuration.ActiveConfig)
        return

######################################################################
    @classmethod
    def IsLinux(cls):
        """
        Returns True if the OS is of Linux type (Debian, Ubuntu, etc.)
        """
        return os.name == "posix"

    ######################################################################
    @classmethod
    def IsWindows(cls):
        """
        Returns True if the OS is a Windows type (Windows 7, etc.)
        """
        return os.name == "nt"

    ######################################################################
    @classmethod
    def get_config_var(cls, var_name):
        try:
            return cls.ActiveConfig[var_name]
        except Exception as ex:
            logger.error("Unable to find configuration variable {0}".format(var_name))
            logger.error(str(ex))
        return None

    ######################################################################
    @classmethod
    def Server(cls):
        return cls.get_config_var("Server")

    ######################################################################
    @classmethod
    def Port(cls):
        return int(cls.get_config_var("Port"))

    ######################################################################
    @classmethod
    def Debug(cls):
        return cls.get_config_var("Debug").lower() == "true"

    ######################################################################
    @classmethod
    def Logconsole(cls):
        return cls.get_config_var("LogConsole").lower() == "true"

    ######################################################################
    @classmethod
    def Logfile(cls):
        return cls.get_config_var("LogFile")

    ######################################################################
    @classmethod
    def LogLevel(cls):
        return cls.get_config_var("LogLevel")

    ######################################################################
    @classmethod
    def DatabasePath(cls):
        return cls.get_config_var("DatabasePath")

    ######################################################################
    @classmethod
    def SecretKey(cls):
        return cls.get_config_var("SecretKey")

    ######################################################################
    @classmethod
    def City(cls):
        return cls.get_config_var("City")

    ######################################################################
    @classmethod
    def Latitude(cls):
        return cls.get_config_var("Latitude")

    ######################################################################
    @classmethod
    def Longitude(cls):
        return cls.get_config_var("Longitude")

    ######################################################################
    @classmethod
    def get_configuration_file_path(cls):
        """
        Returns the full path to the configuration file
        """
        file_name = 'ahps_web.conf'

        # A local configuration file (in the home directory) takes precedent
        if os.path.exists(file_name):
            return file_name

        # Under a *nix system look in /etc
        if Configuration.IsLinux():
            return "/etc/{0}".format(file_name)

        return file_name

    ######################################################################
    @classmethod
    def get_database_file_path(cls, file_name):
        """
        Returns the full path to the SQLite database file
        """
        if Configuration.IsLinux():
            # If a path is not given, use the local copy
            dbpath = Configuration.DatabasePath()
            if dbpath == "":
                # The default when no path is given
                return Configuration.AppPath + "database/" + file_name
            else:
                # A likely place would be /var/local/ahps_web/
                if not dbpath.endswith("/"):
                    dbpath += "/"
                return "{0}{1}".format(dbpath, file_name)
        elif Configuration.IsWindows():
            # Actually, we don't expect to run this on Windows
            return "{0}\\ahps_web\\{1}".format(os.environ["LOCALAPPDATA"], file_name)

        return file_name
