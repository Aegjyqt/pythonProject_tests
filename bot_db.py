import sqlite3


class BotDb:
    """Думаю, разумно создать разные фунцкии на получение админов/пользователей здесь, а не реализовывать это
    в main"""

    _db = sqlite3.connect('bot_users')

    def __init__(self):
        cursor = self._db.cursor()
        try:
            cursor.execute('''
                CREATE TABLE tb_users(id INTEGER PRIMARY KEY, is_admin BOOLEAN)
                ''')
            self._db.commit()

        except sqlite3.OperationalError:
            pass

    def add_to_database(self, user_id: int, is_admin: bool = False) -> None:
        cursor = self._db.cursor()
        try:
            cursor.execute('''
            INSERT INTO tb_users(
            id, is_admin)
            VALUES(?,?)
            ''', (user_id, is_admin))
            self._db.commit()
        except sqlite3.IntegrityError:
            pass

    def get_user_ids(self) -> set:
        cursor = self._db.cursor()
        cursor.execute('''SELECT id, is_admin FROM tb_users''')
        all_rows = cursor.fetchall()
        all_user_ids = set()
        for row in all_rows:
            all_user_ids.add(row[0])
        return all_user_ids

    def get_admin_ids(self) -> set:
        cursor = self._db.cursor()
        cursor.execute('''SELECT id, is_admin FROM tb_users''')
        all_rows = cursor.fetchall()
        admin_ids = set()
        for row in all_rows:
            if row[1]:
                admin_ids.add(row[0])
        return admin_ids


db = BotDb()
