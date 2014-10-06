/*
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
*/

drop table if exists rooms;
drop table if exists modules;
drop table if exists programs;

create table houses (
  houseid integer primary key autoincrement,
  name text not null,
  current integer default 0
);

create table rooms (
  roomid integer primary key autoincrement,
  houseid integer not null,
  name text not null,
  description text default ''
);

create table modules (
  moduleid integer primary key autoincrement,
  roomid integer not null,
  module_type text not null,
  name text not null,
  house_code text not null,
  device_code text not null,
  dim_amount integer default 0
);

create table programs (
  programid integer primary key autoincrement,
  moduleid integer not null,
  name text default '',
  days text default '.......',
  start_trigger_method text default 'none',
  start_time text default '12:00 AM',
  start_offset integer default 0,
  stop_trigger_method text default 'none',
  stop_time text default '12:00 AM',
  stop_offset integer default 0,
  start_randomize integer default 0,
  stop_randomize integer default 0,
  start_randomize_amount integer default 0,
  stop_randomize_amount integer default 0,
  start_action text default 'none',
  stop_action text default 'none',
  start_dim_percent integer default 0,
  stop_dim_percent integer default 0
);


/*
<device module-type="appliance" name="Christmas Lights + Beorne" house-code="B" device-code="12" x="602" y="9">
  <program days="MTWTFSS" start-trigger-method="clock-time" start-time="6:30 PM" start-sunset-offset="0"
  start-sunrise-offset="0" stop-trigger-method="clock-time" stop-time="11:00 PM" stop-sunset-offset="0"
  stop-sunrise-offset="0" start-randomize="0" stop-randomize="0" start-randomize-amount="0" stop-randomize-amount="0"
  start-action="on" stop-action="on" start-dim-percent="0" stop-dim-percent="0" />
</device>
*/