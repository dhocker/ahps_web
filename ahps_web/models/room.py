from ahps_web.database.connection import get_db

def get_rooms():
    '''
    Get all rooms in ascending order by name
    :return: A list of all rooms
    '''
    db = get_db()
    cur = db.execute('select roomid,name,description from rooms order by name asc')
    rooms = cur.fetchall()
    return rooms


def get_room(roomid):
    '''
    Get a room record given its id
    :return: A list of all rooms
    '''
    db = get_db()
    cur = db.execute('select roomid,name,description from rooms where roomid=?', roomid)
    room = cur.fetchall()[0]
    return room


def insert_room(name, desc):
    '''
    Insert a room record
    :return: True if record was created
    '''
    db = get_db()
    db.execute('insert into rooms (name,description) values (?, ?)', [name, desc])
    db.commit()
    return True


def delete_room(roomid):
    '''
    Delete a room record given its roomid
    :return: True if record was deleted
    '''
    db = get_db()
    db.execute('delete from rooms where roomid=?', (roomid,))
    db.commit()
    return True
