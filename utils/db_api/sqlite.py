import sqlite3
from data.config import DB, min_priority


class SQLighter:
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cursor = self.conn.cursor()

    def add_user(self, user_id: int, user_name: str, number: int, priority: int) -> None:
        with self.conn:
            self.cursor.execute("INSERT INTO queue(id, user_name, number, priority) VALUES(?, ?, ?, ?)",
                                (user_id, user_name, number, priority))
            self.cursor.execute("UPDATE queue SET number = number + 1 WHERE priority > ?", (priority,))

    def find_max(self, priority: int, user_id: int = 0) -> int:
        with self.conn:
            if user_id == 0:
                query = "SELECT MAX(number) FROM queue WHERE priority = ?"
                num_tuple = self.cursor.execute(query, (priority,)).fetchone()
                if num_tuple[0] is not None:
                    num = num_tuple[0]
                    max_num = num + 1
                    return max_num
                else:
                    if priority == min_priority:
                        max_num = 1
                        return max_num
                return self.find_max(priority - 1)
            else:
                query = "SELECT MAX(number) FROM queue WHERE priority = ? AND id != ?"
                num_tuple = self.cursor.execute(query, (priority, user_id)).fetchone()
                if num_tuple[0] is not None:
                    num = num_tuple[0]
                    max_num = num + 1
                    return max_num
                else:
                    if priority == min_priority:
                        max_num = 1
                        return max_num
                return self.find_max(priority - 1, user_id)

    def is_present(self, user_id: int):
        with self.conn:
            query = "SELECT id FROM queue WHERE id = ?"
            exists_tp = self.cursor.execute(query, (user_id,)).fetchone()
            if exists_tp is not None:
                return True
        return False

    def get_number(self, user_id: int) -> int:
        with self.conn:
            query = "SELECT number FROM queue WHERE id = ?"
            id_tuple = self.cursor.execute(query, (user_id,)).fetchone()
        num = id_tuple[0]
        return num
