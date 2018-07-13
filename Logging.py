# coding: utf-8
#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright © 2014, 2018  Dave Hocker (email: AtHomeX10@gmail.com)
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

import logging
import logging.handlers
import configuration


# Default overrides
logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
logdateformat = '%Y-%m-%d %H:%M:%S'

formatter = logging.Formatter(logformat, datefmt=logdateformat)

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)

# File handler logging to a fixed file
fh = logging.handlers.TimedRotatingFileHandler("/tmp/ahps_web.log", when='midnight', backupCount=3)


# #######################################################################
# Enable logging for the application startup. This logging is used
# until the configuration file is read. This may seem a bit awkward, but
# you can only log to fixed locations (e.g. console or a specifically
# located file like /tmp/app.log) until the configuration file has been
# read.
def EnableStartupLogging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    # Force log to console
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # Force log to fixed file
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


########################################################################
# Enable logging for the AtHomePowerlineServer application
# In order to get dual logging to work, we'll need to create
# a logger instance in every module that logs. We can configure that
# instance here. In the mean time, we'll use logging to file.
def EnableServerLogging():
    # Logging level override
    log_level_override = configuration.Configuration.LogLevel().lower()
    if log_level_override == "debug":
        loglevel = logging.DEBUG
    elif log_level_override == "info":
        loglevel = logging.INFO
    elif log_level_override == "warn":
        loglevel = logging.WARNING
    elif log_level_override == "error":
        loglevel = logging.ERROR
    else:
        loglevel = logging.DEBUG

    logger = logging.getLogger("app")
    logger.info("Switching to run time server logging")
    logger.setLevel(loglevel)

    # Do we log to console?
    if not configuration.Configuration.Logconsole():
        logger.removeHandler(ch)

    # Do we log to a file?
    logfile = configuration.Configuration.Logfile()
    if logfile != "":
        # Remove the start up handler
        logger.removeHandler(fh)
        # Set up a new run time handler to log to the specified file
        rtfh = logging.handlers.TimedRotatingFileHandler(logfile, when='midnight', backupCount=3)
        rtfh.setLevel(loglevel)
        rtfh.setFormatter(formatter)
        logger.addHandler(rtfh)
        logger.debug("Logging to file: %s", logfile)


# Controlled logging shutdown
def Shutdown():
    logging.shutdown()
    print("Logging shutdown")