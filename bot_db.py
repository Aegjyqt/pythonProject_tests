import sqlite3


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

    def get_user_ids(self) -> set:
        cursor = self._db.cursor()
        cursor.execute('''SELECT id, is_admin FROM tb_users''')
        all_rows = cursor.fetchall()
        all_user_ids = set()
        for row in all_rows:
            all_user_ids.add(row[0])
        cursor.close()
        return all_user_ids

    def get_admin_ids(self) -> set:
        cursor = self._db.cursor()
        cursor.execute('''SELECT id, is_admin FROM tb_users WHERE is_admin=1''')
        all_rows = cursor.fetchall()
        admin_ids = set()
        for row in all_rows:
            admin_ids.add(row[0])
        cursor.close()
        return admin_ids


db = BotDb()
