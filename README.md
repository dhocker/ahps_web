# ahps\_web (AtHomePowerlineServer Web Server)
Copyright © 2015 by Dave Hocker

## Overview

ahps\_web is a companion web server for the AtHomePowerlineServer ([GitHub](https://www.github.com/dhocker/athomepowerlineserver).
It will allow you to control one running instance of the AtHomePowerlineServer from any web browser (it has been tested
with Chrome and Firefox).

Like the AtHomePowerlineServer it was designed to run on a light weight system (e.g. a Raspberry Pi) that can be run head-less
and fan-less. This is as opposed to a PC or Mac based solution. The small size of such a system like the Raspberry Pi allows
it to be positioned more freely (ideally, close to the breaker panel). And, a Raspberry Pi system can be assembled for
considerably less than a PC. While the server was designed to run on a lightweight system, it will run on any system that
supports Python 2.7 (including Windows) and the Flask framework.

Also, like AtHomePowerlineServer application, ahps\_web is open source. Anyone can fork it and build upon it.

## License

The ahps\_web server is licensed under the GNU General Public License v3 as published by the Free Software Foundation, Inc.. See the
LICENSE file for the full text of the license.

## Source Code

The full source is maintained on [GitHub](https://www.github.com/dhocker/ahps\_web).

## Build Environment

ahps\_web is written in Python 2.7. It uses the popular Flask framework.
A suitable development environment would use virtualenv and virtualenvwrapper to create a working virtual environment.
The requirements.txt file can be used with pip to create the required virtual environment with all dependencies.

ahps\_web was developed using PyCharm CE. PyCharm CE is highly recommended. However, a good text editor
of your choice is all that is really required.

## Configuration

To create a working web server, you must assemble a configuration file: ahps\_web.conf. Put this file in the folder where
runserver.py is located. A prototype configuration file can be found in ahps\_web.example.conf.

The ahps\_web.conf file is basically a JSON formatted structure. Here are the keys. To get an idea how the configuration
file is used check out the configuration.py file.

| Key           | Use         |
| ------------- |-------------|
| Debug | True or False. If True, produce more verbose logging. |
| DatabasePath | The path for the folder where the database will be kept. If empty, the default is application_root/database. |
| Server | IP address or name of the AtHomePowerlineServer that is to be controlled. |
| Port | The port number that was assigned to AtHomePowerlineServer. The standard/default is 5000. |
| LogFile | The full path (with file name) of the log file. |
| LogConsole | True or False. If True logging output will be routed to the log file and the console. |
| LogLevel | Debug, Info, Warn, or Error. Case insensitive. |
| SecretKey | The full path (with file name) to the secret key file. Use the make_secret_key.sh script to create a secret key file. |
| City | The name of the city where you are located. Used by the sunrise/sunset dependent code. |
| Latitude | The latitude where you are located. For sunrise/sunset accuracy. |
| Longitude | The longitude where you are located. For sunrise/sunset accuracy. |

## Database

ahps\_web uses Sqlite 3. To get started you need to create an empty database. To do this, run the 
database/init\_db.py script. This will produce an ahps\_web.sqlite3 file. Move the file to the folder designated by the
DatabasePath configuration key.

## Running as an Application

You can run the web server as an application as follows.

1. If you are using virtualenv, activate the environment you set up.
2. Then: python runserver.py

## Running as a Service

The ahps\_webD.sh script can be used to run the web app as a service. That way it will automatically start at boot up time.
If you are not familiar with how to do this, check out this article:
[How to set up a service](http://raspberrywebserver.com/serveradmin/run-a-script-on-start-up.html). Look for the section
titled /etc/init.d.