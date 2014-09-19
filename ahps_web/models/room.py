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