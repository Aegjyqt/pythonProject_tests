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

    def create_table_if_not_exists(self):
        cursor = self._db.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS tb_users(id INTEGER PRIMARY KEY, is_admin BOOLEAN)
                       ''')
        self._db.commit()
        cursor.close()

    def add_to_database(self, user_id: int, is_admin: bool = False) -> None:
        cursor = self._db.cursor()
        cursor.execute('''
                       INSERT OR IGNORE INTO tb_users(
                       id, is_admin)
                       VALUES(?,?)
                       ''', (user_id, is_admin))
        self._db.commit()
        cursor.close()

    def get_users(self) -> list:
        cursor = self._db.cursor()
        cursor.execute('''SELECT id, is_admin FROM tb_users''')
        all_rows = cursor.fetchall()
        users_list = []
        for row in all_rows:
            users_list.append(User(user_id=row[0], is_admin=row[1]))
        return users_list

