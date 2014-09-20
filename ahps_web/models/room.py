from ahps_web.database.connection import get_db

def get_rooms():
    '''
    Get all rooms in ascending order by name
    :return: A list of all rooms
    '''
    db =    get_db()
    cur = db.execute('select roomid,name,description from rooms order by name asc')
    rooms = cur.fetchall()
    return rooms


def get_room(roomid):
    '''
    Get a room record given its id
    :return: A list of all rooms
    '''
    db =    get_db()
    cur = db.execute('select roomid,name,description from rooms where roomid=?', roomid)
    room = cur.fetchall()[0]
    return room