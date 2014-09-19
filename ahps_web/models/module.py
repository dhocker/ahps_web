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