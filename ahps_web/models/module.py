from ahps_web.database.connection import get_db


def get_modules_for_room(roomid):
    '''
    Get all modules for a given room
    :return: A list of modules
    '''
    db =    get_db()
    cur = db.execute('select * from modules where roomid=?', [roomid])
    modules = cur.fetchall()
    return modules


def get_module(moduleid):
    '''
    Get a module record for a given moduleid
    :return: A list of modules
    '''
    db =    get_db()
    cur = db.execute('select * from modules where moduleid=?', [moduleid])
    module = cur.fetchone()
    return module


def update_module_hdc(moduleid, house_code, device_code):
    '''
    Update the hdc for a given module record
    :param moduleid:
    :param house_code:
    :param device_code:
    :return:
    '''
    db = get_db()
    db.execute('update modules set house_code=?, device_code=? where moduleid=?',
               [house_code, device_code, moduleid])
    db.commit()
    return True


def update_module_dim_amount(moduleid, dim_amount):
    '''
    Update the dim amount for a given module record (viable only for lamp module)
    :param moduleid:
    :param dim_amount:
    :return:
    '''
    db = get_db()
    db.execute('update modules set dim_amount=? where moduleid=?',
               [dim_amount, moduleid])
    db.commit()
    return True


def update_module_name(moduleid, name):
    '''
    Update the module name for a given module record
    :param moduleid:
    :param name:
    :return:
    '''
    db = get_db()
    db.execute('update modules set name=? where moduleid=?',
               [name, moduleid])
    db.commit()
    return True


def insert_module(roomid, module_type, name, house_code, device_code, dim_amount=0):
    '''
    Insert a module record
    :return: True if record was created
    '''
    db = get_db()
    db.execute('insert into modules (roomid, module_type, name, house_code, device_code, dim_amount) values (?,?,?,?,?,?)',
               [roomid, module_type, name, house_code, device_code, dim_amount])
    db.commit()
    return True


def delete_module(moduleid):
    '''
    Delete a module record given its moduleid
    :return: True if record was deleted
    '''
    db = get_db()
    db.execute('delete from modules where moduleid=?', (moduleid,))
    db.commit()
    return True
