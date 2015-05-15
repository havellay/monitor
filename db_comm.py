import sqlite3

class Queries(object):
  @staticmethod
  def s_filename_f_quotetab_w_symbol_eq(cursor, s_symbol):
    cursor.execute('SELECT filename from quotetab where symbol=?',[s_symbol])
    return cursor

  @staticmethod
  def i_filename_symbol_i_quotetab(cursor, filename, s_symbol):
    cursor.execute(
        'INSERT INTO quotetab (symbol, filename) VALUES (?, ?)',
        [s_symbol, filename]
      )

  @staticmethod
  def TMP_ct_SYMBOL_w_date_close(cursor, s_symbol):
    cursor.execute('CREATE TABLE ?(date DATE, close REAL)', [s_symbol])
    return cursor

class My_db_class(object):
  db          = []
  db_filename = 'data/db'

  def __init__(self):
    db = sqlite3.connect(self.db_filename)
    self.db.append(db)
    return None

  @staticmethod
  def change_db_filename(filename):
    My_db_class.db_filename = filename
    return None

  @staticmethod
  def get_db():
    return My_db_class.db[0]

  @staticmethod
  def close_db():
    # this is obselete. Use the 'with' keyword.
# refer http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    return My_db_class.db[0].close()
