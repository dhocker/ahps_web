insert into houses (name, current) values ('Test House', 1);

insert into rooms (houseid, name, description) values (1, 'Family Room', 'Family room');

insert into modules (roomid, module_type, name, house_code, device_code) values (1, 'appliance', 'Fireplace Left', 'a', '1');
insert into modules (roomid, module_type, name, house_code, device_code) values (1, 'appliance', 'Fireplace Right', 'a', '2');

insert into rooms (houseid, name, description) values (1, 'Studio', 'Dave''s office and studio');

insert into modules (roomid, module_type, name, house_code, device_code) values (2, 'appliance', 'Harvest Tree', 'A', '7');
insert into modules (roomid, module_type, name, house_code, device_code) values (2, 'lamp', 'Corner Light', 'L', '1');
