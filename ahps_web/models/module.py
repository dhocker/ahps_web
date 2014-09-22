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


def insert_module(roomid, module_type, name, house_code, device_code):
    '''
    Insert a module record
    :return: True if record was created
    '''
    db = get_db()
    db.execute('insert into modules (roomid, module_type, name, house_code, device_code) values (?,?,?,?,?)',
               [roomid, module_type, name, house_code, device_code])
    db.commit()
    return True