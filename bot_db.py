import contextlib
import sqlite3
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    is_admin: bool


class BotDb:

    def __init__(self):
        self._db = sqlite3.connect('bot_users')
        self.create_table_if_not_exists()

    @contextlib.contextmanager
    def db_access(self):
        cursor = self._db.cursor()
        yield cursor
        cursor.close()

    def create_table_if_not_exists(self):
        with self.db_access() as cursor:
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS tbl_users(id INTEGER PRIMARY KEY, is_admin BOOLEAN)
                           ''')
            self._db.commit()

    def add_to_database(self, user_id: int, is_admin: bool = False) -> None:
        with self.db_access() as cursor:
            cursor.execute('''
                           INSERT OR IGNORE INTO tbl_users(
                           id, is_admin)
                           VALUES(?,?)
                           ''', (user_id, is_admin))
            self._db.commit()

    def get_regular_users(self) -> list:
        with self.db_access() as cursor:
            cursor.execute('''SELECT id, is_admin FROM tbl_users WHERE is_admin = 0''')
            all_rows = cursor.fetchall()
            regular_users_list = []
            for row in all_rows:
                regular_users_list.append(User(user_id=row[0], is_admin=row[1]))
        return regular_users_list

    def get_admins(self) -> list:
        with self.db_access() as cursor:
            cursor.execute('''SELECT id, is_admin FROM tbl_users WHERE is_admin = 1''')
            all_rows = cursor.fetchall()
            admins_list = []
            for row in all_rows:
                admins_list.append(User(user_id=row[0], is_admin=row[1]))
        return admins_list
