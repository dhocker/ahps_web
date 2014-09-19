drop table if exists rooms;
drop table if exists modules;

create table rooms (
  roomid integer primary key autoincrement,
  name text not null,
  description text not null
);

create table modules (
  moduleid integer primary key autoincrement,
  roomid integer not null,
  moduletype text not null,
  name text not null,
  housecode text not null,
  devicecode text not null
);

insert into rooms (name, description) values ('Family Room', 'Family room');

insert into modules (roomid, moduletype, name, housecode, devicecode) values (1, 'appliance', 'Fireplace Left', 'a', '1');
insert into modules (roomid, moduletype, name, housecode, devicecode) values (1, 'appliance', 'Fireplace Right', 'a', '2');

insert into rooms (name, description) values ('Studio', 'Dave''s office and studio');

insert into modules (roomid, moduletype, name, housecode, devicecode) values (2, 'appliance', 'Harvest Tree', 'A', '7');
insert into modules (roomid, moduletype, name, housecode, devicecode) values (2, 'lamp', 'Corner Light', 'L', '1');
