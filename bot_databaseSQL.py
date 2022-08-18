import sqlite3

db = sqlite3.connect('bot_users_db')

cursor = db.cursor()

try:
    cursor.execute('''
        CREATE TABLE bot_users_db(id INTEGER PRIMARY KEY, user_id TEXT unique, user_type TEXT)
        ''')
    db.commit()
except sqlite3.OperationalError:
    pass


async def add_to_database(user_id, user_type='user') -> None:
    try:
        cursor.execute('''
        INSERT INTO bot_users_db(
        user_id, user_type)
        VALUES(?,?)
        ''', (user_id, user_type))
        db.commit()
    except sqlite3.IntegrityError:
        pass


def get_user_ids() -> list:
    cursor.execute('''SELECT user_id, user_type FROM bot_users_db''')
    all_rows = cursor.fetchall()
    all_user_ids = []
    for row in all_rows:
        all_user_ids.append(row[0])
    return all_user_ids
