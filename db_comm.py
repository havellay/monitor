import sqlite3

class My_db_class():
    db = None
    file_name = 'data\/mydb'

    def __init__(self):
        self.db = sqlite3.connect(self.file_name)
        return self.db

    def get_db(self):
        if db is None:
            init_db()
        return db

    def close_db():
        # this is obselete. Use the 'with' keyword.
# refer http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
        return self.db.close()
