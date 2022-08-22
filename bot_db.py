import sqlite3


class BotDb: 
    """Думаю, разумно создать разные фунцкии на получение админов/пользователей здесь, а не реализовывать это
    в main"""

    def __init__(self):
        self._db = sqlite3.connect('bot_users.db')

    def __enter__(self):
        self._create_table_if_not_exists()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()

    def _create_table_if_not_exists(self):
        # Создан коннект к базе:
        cursor = self._db.cursor()
        try:
            # Почитать про SQL проверку IF NOT EXISTS
            cursor.execute('''
                        CREATE TABLE tbl_users(id INTEGER PRIMARY KEY, is_admin BOOLEAN)
                        ''')
            self._db.commit()
            # Закрыт коннект к базе:
            cursor.close()

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
            cursor.close()
        except sqlite3.IntegrityError as e:
            print(e)

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
        cursor.execute('''SELECT id, is_admin FROM tbl_users WHERE is_admin = True''')
        all_rows = cursor.fetchall()
        admin_ids = set()
        for row in all_rows:
            if row[1]:
                admin_ids.add(row[0])
        return admin_ids

    def close(self) -> None:
        self._db.close()

# TODO: Реализовать контекстный менеджер с этим классом (__enter__, __exit__).
# TODO: Реализовать маппинг данных из базы к объекту (датаклассу).
