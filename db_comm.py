import sqlite3

class My_db_class():
    db = None
    file_name = 'data\/mydb'

    def __init__(self):
        return init_db()

    def get_db(self):
        if db is None:
            init_db()
        return db

    @staticmethod
    def init_db(self):
        if self.db is None:
            self.db = sqlite3.connect(file_name)
        return self.db

    def close_db():
        return self.db.close()
